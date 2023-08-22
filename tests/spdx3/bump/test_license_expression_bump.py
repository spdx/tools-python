# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import pytest
from license_expression import LicenseExpression

from spdx_tools.common.spdx_licensing import spdx_licensing
from spdx_tools.spdx3.bump_from_spdx2.license_expression import (
    bump_license_expression,
    bump_license_expression_or_none_or_no_assertion,
)
from spdx_tools.spdx3.model.licensing import (
    ConjunctiveLicenseSet,
    CustomLicense,
    CustomLicenseAddition,
    DisjunctiveLicenseSet,
    ListedLicense,
    ListedLicenseException,
    NoAssertionLicense,
    NoneLicense,
    WithAdditionOperator,
)
from spdx_tools.spdx.model import SpdxNoAssertion, SpdxNone
from tests.spdx.fixtures import extracted_licensing_info_fixture


@pytest.mark.parametrize(
    "element, expected_class",
    [
        (SpdxNoAssertion(), NoAssertionLicense),
        (SpdxNone(), NoneLicense),
        (spdx_licensing.parse("MIT"), ListedLicense),
    ],
)
def test_license_expression_or_none_or_no_assertion(element, expected_class):
    license_info = bump_license_expression_or_none_or_no_assertion(element, [])

    assert isinstance(license_info, expected_class)


@pytest.mark.parametrize(
    "license_expression, extracted_licensing_info, expected_element",
    [
        (spdx_licensing.parse("MIT"), [], ListedLicense("MIT", "MIT", "blank")),
        (spdx_licensing.parse("LGPL-2.0"), [], ListedLicense("LGPL-2.0-only", "LGPL-2.0-only", "blank")),
        (
            spdx_licensing.parse("LicenseRef-1"),
            [extracted_licensing_info_fixture()],
            CustomLicense("LicenseRef-1", "licenseName", "extractedText"),
        ),
        (
            spdx_licensing.parse("MIT AND LGPL-2.0"),
            [],
            ConjunctiveLicenseSet(
                [ListedLicense("MIT", "MIT", "blank"), ListedLicense("LGPL-2.0-only", "LGPL-2.0-only", "blank")]
            ),
        ),
        (
            spdx_licensing.parse("LicenseRef-1 OR LGPL-2.0"),
            [extracted_licensing_info_fixture()],
            DisjunctiveLicenseSet(
                [
                    CustomLicense("LicenseRef-1", "licenseName", "extractedText"),
                    ListedLicense("LGPL-2.0-only", "LGPL-2.0-only", "blank"),
                ]
            ),
        ),
        (
            spdx_licensing.parse("LGPL-2.0 WITH 389-exception"),
            [],
            WithAdditionOperator(
                ListedLicense("LGPL-2.0-only", "LGPL-2.0-only", "blank"),
                ListedLicenseException("389-exception", "", ""),
            ),
        ),
        (
            spdx_licensing.parse("LicenseRef-1 WITH custom-exception"),
            [
                extracted_licensing_info_fixture(),
                extracted_licensing_info_fixture("custom-exception", "This is a custom exception", "exceptionName"),
            ],
            WithAdditionOperator(
                CustomLicense("LicenseRef-1", "licenseName", "extractedText"),
                CustomLicenseAddition("custom-exception", "exceptionName", "This is a custom exception"),
            ),
        ),
        (
            spdx_licensing.parse("MIT AND LicenseRef-1 WITH custom-exception"),
            [
                extracted_licensing_info_fixture(),
                extracted_licensing_info_fixture("custom-exception", "This is a custom exception", "exceptionName"),
            ],
            ConjunctiveLicenseSet(
                [
                    ListedLicense("MIT", "MIT", "blank"),
                    WithAdditionOperator(
                        CustomLicense("LicenseRef-1", "licenseName", "extractedText"),
                        CustomLicenseAddition("custom-exception", "exceptionName", "This is a custom exception"),
                    ),
                ]
            ),
        ),
    ],
)
def test_license_expression_bump(license_expression: LicenseExpression, extracted_licensing_info, expected_element):
    license_info = bump_license_expression(license_expression, extracted_licensing_info)

    assert license_info == expected_element
