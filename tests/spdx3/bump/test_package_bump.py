# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from unittest import TestCase, mock

from spdx_tools.spdx3.bump_from_spdx2.package import bump_package
from spdx_tools.spdx3.model import ExternalIdentifier, ExternalIdentifierType, ExternalReference, ExternalReferenceType
from spdx_tools.spdx3.model.software import Package
from spdx_tools.spdx3.payload import Payload
from spdx_tools.spdx.model.package import ExternalPackageRef, ExternalPackageRefCategory
from spdx_tools.spdx.model.package import Package as Spdx2_Package
from tests.spdx.fixtures import package_fixture


@mock.patch("spdx_tools.spdx3.model.CreationInformation")
def test_bump_package(creation_information):
    payload = Payload()
    document_namespace = "https://doc.namespace"
    spdx2_package: Spdx2_Package = package_fixture(
        external_references=[
            ExternalPackageRef(
                ExternalPackageRefCategory.SECURITY, "advisory", "advisory_locator", "advisory_comment"
            ),
            ExternalPackageRef(ExternalPackageRefCategory.PERSISTENT_ID, "swh", "swh_locator", "swh_comment"),
        ]
    )
    expected_new_package_id = f"{document_namespace}#{spdx2_package.spdx_id}"

    bump_package(spdx2_package, payload, creation_information, document_namespace)
    package = payload.get_element(expected_new_package_id)

    assert isinstance(package, Package)
    assert package.spdx_id == expected_new_package_id
    assert package.package_version == spdx2_package.version
    assert package.external_references == [
        ExternalReference(ExternalReferenceType.SECURITY_ADVISORY, ["advisory_locator"], None, "advisory_comment")
    ]
    assert package.external_identifier == [
        ExternalIdentifier(ExternalIdentifierType.SWHID, "swh_locator", "swh_comment")
    ]
    assert package.download_location == spdx2_package.download_location
    assert package.package_version == spdx2_package.version
    assert package.homepage == spdx2_package.homepage
    assert package.source_info == spdx2_package.source_info
    assert package.built_time == spdx2_package.built_date
    assert package.release_time == spdx2_package.release_date
    assert package.valid_until_time == spdx2_package.valid_until_date


@mock.patch("spdx_tools.spdx3.model.CreationInformation")
def test_bump_of_single_purl_without_comment(creation_information):
    payload = Payload()
    document_namespace = "https://doc.namespace"
    spdx2_package: Spdx2_Package = package_fixture(
        external_references=[
            ExternalPackageRef(ExternalPackageRefCategory.PACKAGE_MANAGER, "purl", "purl_locator", None),
        ]
    )
    expected_new_package_id = f"{document_namespace}#{spdx2_package.spdx_id}"

    bump_package(spdx2_package, payload, creation_information, document_namespace)
    package = payload.get_element(expected_new_package_id)

    assert package.package_url == "purl_locator"
    assert package.external_references == []
    assert package.external_identifier == []


@mock.patch("spdx_tools.spdx3.model.CreationInformation")
def test_bump_of_single_purl_with_comment(creation_information):
    payload = Payload()
    document_namespace = "https://doc.namespace"
    spdx2_package: Spdx2_Package = package_fixture(
        external_references=[
            ExternalPackageRef(ExternalPackageRefCategory.PACKAGE_MANAGER, "purl", "purl_locator", "purl_comment"),
        ]
    )
    expected_new_package_id = f"{document_namespace}#{spdx2_package.spdx_id}"

    bump_package(spdx2_package, payload, creation_information, document_namespace)
    package = payload.get_element(expected_new_package_id)

    assert package.package_url is None
    assert package.external_references == []
    assert package.external_identifier == [
        ExternalIdentifier(ExternalIdentifierType.PURL, "purl_locator", "purl_comment")
    ]


@mock.patch("spdx_tools.spdx3.model.CreationInformation")
def test_bump_of_multiple_purls(creation_information):
    payload = Payload()
    document_namespace = "https://doc.namespace"
    spdx2_package: Spdx2_Package = package_fixture(
        external_references=[
            ExternalPackageRef(ExternalPackageRefCategory.PACKAGE_MANAGER, "purl", "purl_locator", "comment"),
            ExternalPackageRef(ExternalPackageRefCategory.PACKAGE_MANAGER, "purl", "purl_locator2", None),
        ]
    )
    expected_new_package_id = f"{document_namespace}#{spdx2_package.spdx_id}"

    bump_package(spdx2_package, payload, creation_information, document_namespace)
    package = payload.get_element(expected_new_package_id)

    assert package.package_url is None
    assert package.external_references == []
    TestCase().assertCountEqual(
        package.external_identifier,
        [
            ExternalIdentifier(ExternalIdentifierType.PURL, "purl_locator", "comment"),
            ExternalIdentifier(ExternalIdentifierType.PURL, "purl_locator2", None),
        ],
    )
