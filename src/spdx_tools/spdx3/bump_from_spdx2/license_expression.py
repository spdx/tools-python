# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from typing import Union

from license_expression import (
    AND,
    OR,
    LicenseExpression,
    LicenseSymbol,
    LicenseWithExceptionSymbol,
    get_spdx_licensing,
)

from spdx_tools.spdx3.model.licensing import (
    AnyLicenseInfo,
    ConjunctiveLicenseSet,
    CustomLicense,
    CustomLicenseAddition,
    DisjunctiveLicenseSet,
    License,
    LicenseAddition,
    LicenseField,
    ListedLicense,
    ListedLicenseException,
    NoAssertionLicense,
    NoneLicense,
    WithAdditionOperator,
)
from spdx_tools.spdx.model import SpdxNoAssertion, SpdxNone


def bump_license_expression_or_none_or_no_assertion(
    element: Union[LicenseExpression, SpdxNoAssertion, SpdxNone]
) -> LicenseField:
    if isinstance(element, SpdxNone):
        return NoneLicense()
    elif isinstance(element, SpdxNoAssertion):
        return NoAssertionLicense()
    else:
        return bump_license_expression(element)


def bump_license_expression(license_expression: LicenseExpression) -> AnyLicenseInfo:
    if isinstance(license_expression, AND):
        return ConjunctiveLicenseSet(member=[bump_license_expression(element) for element in license_expression.args])
    if isinstance(license_expression, OR):
        return DisjunctiveLicenseSet(member=[bump_license_expression(element) for element in license_expression.args])
    if isinstance(license_expression, LicenseWithExceptionSymbol):
        subject_license = bump_license_expression(license_expression.license_symbol)
        if not isinstance(subject_license, License):
            raise ValueError("Subject of LicenseException couldn't be converted to License.")
        return WithAdditionOperator(
            subject_license=subject_license,
            subject_addition=bump_license_exception(license_expression.exception_symbol),
        )
    if isinstance(license_expression, LicenseSymbol):
        if not get_spdx_licensing().validate(license_expression).invalid_symbols:
            return ListedLicense(license_expression.key, license_expression.obj, "")
        else:
            return CustomLicense(license_expression.key, "", "")


def bump_license_exception(license_exception: LicenseSymbol) -> LicenseAddition:
    if not get_spdx_licensing().validate(license_exception).invalid_symbols:
        return ListedLicenseException(license_exception.key, "", "")
    else:
        return CustomLicenseAddition(license_exception.key, "", "")
