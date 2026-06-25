# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import pytest
from license_expression import LicenseExpression

from spdx_tools.common.spdx_licensing import spdx_licensing
from spdx_tools.spdx3.bump_from_spdx2.license_expression import (
    bump_license_expression,
)
from spdx_tools.spdx3.model.expandedlicensing import (
    ConjunctiveLicenseSet,
    CustomLicense,
    DisjunctiveLicenseSet,
    ListedLicense,
    WithAdditionOperator,
)
from spdx_tools.spdx3.payload import Payload
from tests.spdx3.fixtures import creation_info_fixture
from tests.spdx.fixtures import extracted_licensing_info_fixture

creation_info = creation_info_fixture()

namespace = "https://doc.namespace"


@pytest.mark.parametrize(
    "license_expression, extracted_licensing_info, expected_element",
    [
        (
            spdx_licensing.parse("MIT"),
            [],
            ListedLicense("https://doc.namespace#SPDXRef-ListedLicense-1", "blank", creation_info, name="MIT"),
        ),
        (
            spdx_licensing.parse("LGPL-2.0"),
            [],
            ListedLicense(
                "https://doc.namespace#SPDXRef-ListedLicense-1", "blank", creation_info, name="LGPL-2.0-only"
            ),
        ),
        (
            spdx_licensing.parse("LicenseRef-1"),
            [extracted_licensing_info_fixture()],
            CustomLicense(
                "https://doc.namespace#SPDXRef-CustomLicense-1", "extractedText", creation_info, name="licenseName"
            ),
        ),
        (
            spdx_licensing.parse("MIT AND LGPL-2.0"),
            [],
            ConjunctiveLicenseSet(
                "https://doc.namespace#SPDXRef-ConjunctiveLicenseSet-0",
                [
                    "https://doc.namespace#SPDXRef-ListedLicense-1",
                    "https://doc.namespace#SPDXRef-ListedLicense-2",
                ],
                creation_info,
            ),
        ),
        (
            spdx_licensing.parse("LicenseRef-1 OR LGPL-2.0"),
            [extracted_licensing_info_fixture()],
            DisjunctiveLicenseSet(
                "https://doc.namespace#SPDXRef-DisjunctiveLicenseSet-1",
                [
                    "https://doc.namespace#SPDXRef-CustomLicense-1",
                    "https://doc.namespace#SPDXRef-ListedLicense-1",
                ],
                creation_info,
            ),
        ),
        (
            spdx_licensing.parse("LGPL-2.0 WITH 389-exception"),
            [],
            WithAdditionOperator(
                "https://doc.namespace#SPDXRef-WithAdditionOperator-0",
                "https://doc.namespace#SPDXRef-ListedLicense-1",
                "https://doc.namespace#SPDXRef-ListedLicenseException-0",
                creation_info,
            ),
        ),
        (
            spdx_licensing.parse("LicenseRef-1 WITH custom-exception"),
            [
                extracted_licensing_info_fixture(),
                extracted_licensing_info_fixture("custom-exception", "This is a custom exception", "exceptionName"),
            ],
            WithAdditionOperator(
                "https://doc.namespace#SPDXRef-WithAdditionOperator-0",
                "https://doc.namespace#SPDXRef-CustomLicense-1",
                "https://doc.namespace#SPDXRef-CustomLicenseAddition-0",
                creation_info,
            ),
        ),
        (
            spdx_licensing.parse("MIT AND LicenseRef-1 WITH custom-exception"),
            [
                extracted_licensing_info_fixture(),
                extracted_licensing_info_fixture("custom-exception", "This is a custom exception", "exceptionName"),
            ],
            ConjunctiveLicenseSet(
                "https://doc.namespace#SPDXRef-ConjunctiveLicenseSet-0",
                [
                    "https://doc.namespace#SPDXRef-ListedLicense-1",
                    "https://doc.namespace#SPDXRef-WithAdditionOperator-0",
                ],
                creation_info,
            ),
        ),
    ],
)
def test_license_expression_bump(license_expression: LicenseExpression, extracted_licensing_info, expected_element):
    # populating the payload to test that additional SPDX IDs belonging to elements of these types increment correctly
    payload = Payload()
    payload.add_element(
        CustomLicense("https://doc.namespace#SPDXRef-CustomLicense-0", "license text", creation_info_fixture())
    )
    payload.add_element(
        ListedLicense("https://doc.namespace#SPDXRef-ListedLicense-0", "license text", creation_info_fixture())
    )
    payload.add_element(
        DisjunctiveLicenseSet(
            "https://doc.namespace#SPDXRef-DisjunctiveLicenseSet-0",
            [
                "https://doc.namespace#SPDXRef-CustomLicense-0",
                "https://doc.namespace#SPDXRef-ListedLicense-0",
            ],
            creation_info,
        )
    )
    license_info = bump_license_expression(
        license_expression, extracted_licensing_info, namespace, creation_info, payload
    )

    assert license_info == expected_element
