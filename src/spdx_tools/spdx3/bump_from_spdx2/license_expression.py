# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from beartype.typing import List, Union
from license_expression import AND, OR, LicenseExpression, LicenseSymbol, LicenseWithExceptionSymbol

from spdx_tools.common.spdx_licensing import spdx_licensing
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
from spdx_tools.spdx.model import ExtractedLicensingInfo, SpdxNoAssertion, SpdxNone


def bump_license_expression_or_none_or_no_assertion(
    element: Union[LicenseExpression, SpdxNoAssertion, SpdxNone],
    extracted_licensing_info: List[ExtractedLicensingInfo],
) -> LicenseField:
    if isinstance(element, SpdxNone):
        return NoneLicense()
    elif isinstance(element, SpdxNoAssertion):
        return NoAssertionLicense()
    else:
        return bump_license_expression(element, extracted_licensing_info)


def bump_license_expression(
    license_expression: LicenseExpression, extracted_licensing_info: List[ExtractedLicensingInfo]
) -> AnyLicenseInfo:
    if isinstance(license_expression, AND):
        return ConjunctiveLicenseSet(
            member=[bump_license_expression(element, extracted_licensing_info) for element in license_expression.args]
        )
    if isinstance(license_expression, OR):
        return DisjunctiveLicenseSet(
            member=[bump_license_expression(element, extracted_licensing_info) for element in license_expression.args]
        )
    if isinstance(license_expression, LicenseWithExceptionSymbol):
        subject_license = bump_license_expression(license_expression.license_symbol, extracted_licensing_info)
        if not isinstance(subject_license, License):
            raise ValueError("Subject of LicenseException couldn't be converted to License.")
        return WithAdditionOperator(
            subject_license=subject_license,
            subject_addition=bump_license_exception(license_expression.exception_symbol, extracted_licensing_info),
        )
    if isinstance(license_expression, LicenseSymbol):
        if not spdx_licensing.validate(license_expression).invalid_symbols:
            return ListedLicense(license_expression.key, license_expression.obj, "blank")
        else:
            for licensing_info in extracted_licensing_info:
                if licensing_info.license_id == license_expression.key:
                    # the fields are optional in ExtractedLicensingInfo, to prevent type errors we use a type
                    # conversion to str as a quick fix
                    return CustomLicense(
                        str(licensing_info.license_id),
                        str(licensing_info.license_name),
                        str(licensing_info.extracted_text),
                    )

            return CustomLicense(license_expression.key, "", "")


def bump_license_exception(
    license_exception: LicenseSymbol, extracted_licensing_info: List[ExtractedLicensingInfo]
) -> LicenseAddition:
    if not spdx_licensing.validate(license_exception).invalid_symbols:
        return ListedLicenseException(license_exception.key, "", "")
    else:
        for licensing_info in extracted_licensing_info:
            if licensing_info.license_id == license_exception.key:
                # the fields are optional in ExtractedLicensingInfo, to prevent type errors we use a type conversion
                # to str as a quick fix
                return CustomLicenseAddition(
                    str(licensing_info.license_id),
                    str(licensing_info.license_name),
                    str(licensing_info.extracted_text),
                )
        return CustomLicenseAddition(license_exception.key, "", "")
