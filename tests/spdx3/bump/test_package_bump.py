# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from unittest import TestCase

import pytest

from spdx_tools.spdx3.bump_from_spdx2.package import bump_package
from spdx_tools.spdx3.model import ExternalIdentifier, ExternalIdentifierType, ExternalReference, ExternalReferenceType
from spdx_tools.spdx3.model.software import Package
from spdx_tools.spdx3.payload import Payload
from spdx_tools.spdx.model import SpdxNoAssertion
from spdx_tools.spdx.model.package import ExternalPackageRef, ExternalPackageRefCategory
from spdx_tools.spdx.model.package import Package as Spdx2_Package
from tests.spdx.fixtures import actor_fixture, package_fixture


@pytest.mark.parametrize(
    "originator, expected_originator, supplier, expected_supplier",
    [
        (
            actor_fixture(name="originatorName"),
            ["https://doc.namespace#SPDXRef-Actor-originatorName-some@mail.com"],
            actor_fixture(name="supplierName"),
            ["https://doc.namespace#SPDXRef-Actor-supplierName-some@mail.com"],
        ),
        (None, [], None, []),
        (SpdxNoAssertion(), [], SpdxNoAssertion(), []),
    ],
)
def test_bump_package(originator, expected_originator, supplier, expected_supplier):
    payload = Payload()
    document_namespace = "https://doc.namespace"
    spdx2_package: Spdx2_Package = package_fixture(
        originator=originator,
        supplier=supplier,
        external_references=[
            ExternalPackageRef(
                ExternalPackageRefCategory.SECURITY, "advisory", "advisory_locator", "advisory_comment"
            ),
            ExternalPackageRef(ExternalPackageRefCategory.PERSISTENT_ID, "swh", "swh_locator", "swh_comment"),
        ],
    )
    expected_new_package_id = f"{document_namespace}#{spdx2_package.spdx_id}"

    bump_package(spdx2_package, payload, document_namespace, [], [])
    package = payload.get_element(expected_new_package_id)

    assert isinstance(package, Package)
    assert package.spdx_id == expected_new_package_id
    assert package.package_version == spdx2_package.version
    assert package.external_reference == [
        ExternalReference(ExternalReferenceType.SECURITY_ADVISORY, ["advisory_locator"], None, "advisory_comment")
    ]
    assert package.external_identifier == [
        ExternalIdentifier(ExternalIdentifierType.SWHID, "swh_locator", "swh_comment")
    ]
    assert package.download_location == spdx2_package.download_location
    assert package.package_version == spdx2_package.version
    assert package.originated_by == expected_originator
    assert package.supplied_by == expected_supplier
    assert package.homepage == spdx2_package.homepage
    assert package.source_info == spdx2_package.source_info
    assert package.built_time == spdx2_package.built_date
    assert package.release_time == spdx2_package.release_date
    assert package.valid_until_time == spdx2_package.valid_until_date
    assert package.copyright_text == spdx2_package.copyright_text
    assert package.attribution_text == spdx2_package.attribution_texts[0]


def test_bump_of_single_purl_without_comment():
    payload = Payload()
    document_namespace = "https://doc.namespace"
    spdx2_package: Spdx2_Package = package_fixture(
        external_references=[
            ExternalPackageRef(ExternalPackageRefCategory.PACKAGE_MANAGER, "purl", "purl_locator", None),
        ]
    )
    expected_new_package_id = f"{document_namespace}#{spdx2_package.spdx_id}"

    bump_package(spdx2_package, payload, document_namespace, [], [])
    package = payload.get_element(expected_new_package_id)

    assert package.package_url == "purl_locator"
    assert package.external_reference == []
    assert package.external_identifier == []


def test_bump_of_single_purl_with_comment():
    payload = Payload()
    document_namespace = "https://doc.namespace"
    spdx2_package: Spdx2_Package = package_fixture(
        external_references=[
            ExternalPackageRef(ExternalPackageRefCategory.PACKAGE_MANAGER, "purl", "purl_locator", "purl_comment"),
        ]
    )
    expected_new_package_id = f"{document_namespace}#{spdx2_package.spdx_id}"

    bump_package(spdx2_package, payload, document_namespace, [], [])
    package = payload.get_element(expected_new_package_id)

    assert package.package_url is None
    assert package.external_reference == []
    assert package.external_identifier == [
        ExternalIdentifier(ExternalIdentifierType.PURL, "purl_locator", "purl_comment")
    ]


def test_bump_of_multiple_purls():
    payload = Payload()
    document_namespace = "https://doc.namespace"
    spdx2_package: Spdx2_Package = package_fixture(
        external_references=[
            ExternalPackageRef(ExternalPackageRefCategory.PACKAGE_MANAGER, "purl", "purl_locator", "comment"),
            ExternalPackageRef(ExternalPackageRefCategory.PACKAGE_MANAGER, "purl", "purl_locator2", None),
        ]
    )
    expected_new_package_id = f"{document_namespace}#{spdx2_package.spdx_id}"

    bump_package(spdx2_package, payload, document_namespace, [], [])
    package = payload.get_element(expected_new_package_id)

    assert package.package_url is None
    assert package.external_reference == []
    TestCase().assertCountEqual(
        package.external_identifier,
        [
            ExternalIdentifier(ExternalIdentifierType.PURL, "purl_locator", "comment"),
            ExternalIdentifier(ExternalIdentifierType.PURL, "purl_locator2", None),
        ],
    )
