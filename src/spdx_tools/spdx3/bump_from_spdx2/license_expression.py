# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from typing import List

from license_expression import AND, OR, LicenseExpression, LicenseSymbol, LicenseWithExceptionSymbol

from spdx_tools.common.spdx_licensing import spdx_licensing
from spdx_tools.spdx3.model.creation_info import CreationInfo
from spdx_tools.spdx3.model.element import Element
from spdx_tools.spdx3.model.expandedlicensing import (
    ConjunctiveLicenseSet,
    CustomLicense,
    CustomLicenseAddition,
    DisjunctiveLicenseSet,
    License,
    LicenseAddition,
    ListedLicense,
    ListedLicenseException,
    WithAdditionOperator,
)
from spdx_tools.spdx3.model.simplelicensing.any_license_info import AnyLicenseInfo
from spdx_tools.spdx3.payload import Payload
from spdx_tools.spdx.model import ExtractedLicensingInfo

LICENSE_EXPRESSION_TYPES = {
    ConjunctiveLicenseSet,
    DisjunctiveLicenseSet,
    LicenseWithExceptionSymbol,
    WithAdditionOperator,
    ListedLicense,
    CustomLicense,
    ListedLicenseException,
    CustomLicenseAddition,
}


def _get_spdx_id_for_license_expression(
    license_expression_type: type, document_namespace: str, license_element_counts: dict[type, int]
) -> str:
    number_of_existing_elements_of_type = license_element_counts.get(license_expression_type, 0)

    return f"{document_namespace}#SPDXRef-{license_expression_type.__name__}-{number_of_existing_elements_of_type}"


def _get_count_of_license_expression_types(license_expression_types: set[type], payload: Payload) -> dict[type, int]:
    license_element_counts: dict[type, int] = {}

    for element_type in payload.get_full_map().values():
        if type(element_type) in license_expression_types:
            license_element_counts[type(element_type)] = license_element_counts.get(type(element_type), 0) + 1

    return license_element_counts


# Convenience method since this code block is called multiple times in this file
def _add_license(license: Element, payload: Payload, license_element_counts: dict[type, int]) -> None:
    license_type = type(license)
    payload.add_element(license)
    license_element_counts[license_type] = license_element_counts.get(license_type, 0) + 1


# TODO make this raise an exception if the license expression contains NOASSERTION or NONE,
# as they are apparently not supported in SPDX 3.0
def bump_license_expression(
    license_expression: LicenseExpression,
    extracted_licensing_info: List[ExtractedLicensingInfo],
    document_namespace: str,
    creation_info: CreationInfo,
    payload: Payload,
    license_element_counts: (
        dict[type, int] | None
    ) = None,  # do not use this argument unless already inside a bump_license_expression
) -> AnyLicenseInfo:

    if not license_element_counts:
        license_element_counts = _get_count_of_license_expression_types(LICENSE_EXPRESSION_TYPES, payload)

    if isinstance(license_expression, AND):
        license = ConjunctiveLicenseSet(
            _get_spdx_id_for_license_expression(ConjunctiveLicenseSet, document_namespace, license_element_counts),
            member=[
                bump_license_expression(
                    element,
                    extracted_licensing_info,
                    document_namespace,
                    creation_info,
                    payload,
                    license_element_counts,
                ).spdx_id
                for element in license_expression.args
            ],
            creation_info=creation_info,
        )
        _add_license(license, payload, license_element_counts)
        return license
    if isinstance(license_expression, OR):
        license = DisjunctiveLicenseSet(
            _get_spdx_id_for_license_expression(DisjunctiveLicenseSet, document_namespace, license_element_counts),
            creation_info=creation_info,
            member=[
                bump_license_expression(
                    element,
                    extracted_licensing_info,
                    document_namespace,
                    creation_info,
                    payload,
                    license_element_counts,
                ).spdx_id
                for element in license_expression.args
            ],
        )
        _add_license(license, payload, license_element_counts)
        return license
    if isinstance(license_expression, LicenseWithExceptionSymbol):
        subject_license = bump_license_expression(
            license_expression.license_symbol,
            extracted_licensing_info,
            document_namespace,
            creation_info,
            payload,
            license_element_counts,
        )
        if not isinstance(subject_license, License):
            raise ValueError("Subject of LicenseException couldn't be converted to License.")
        license = WithAdditionOperator(
            _get_spdx_id_for_license_expression(WithAdditionOperator, document_namespace, license_element_counts),
            subject_extendable_license=subject_license.spdx_id,
            subject_addition=bump_license_exception(
                license_expression.exception_symbol,
                extracted_licensing_info,
                document_namespace,
                creation_info,
                payload,
                license_element_counts,
            ).spdx_id,
            creation_info=creation_info,
        )
        _add_license(license, payload, license_element_counts)
        return license
    if isinstance(license_expression, LicenseSymbol):
        if not spdx_licensing.validate(license_expression).invalid_symbols:
            license = ListedLicense(
                _get_spdx_id_for_license_expression(ListedLicense, document_namespace, license_element_counts),
                "blank",
                creation_info,
                name=license_expression.obj,
            )
            _add_license(license, payload, license_element_counts)
            return license
        else:
            for licensing_info in extracted_licensing_info:
                if licensing_info.license_id == license_expression.key:
                    # the fields are optional in ExtractedLicensingInfo, to prevent type errors we use a type
                    # conversion to str as a quick fix
                    license = CustomLicense(
                        _get_spdx_id_for_license_expression(CustomLicense, document_namespace, license_element_counts),
                        str(licensing_info.extracted_text),
                        creation_info,
                        name=str(licensing_info.license_name),
                    )
                    _add_license(license, payload, license_element_counts)
                    return license

            license = CustomLicense(
                _get_spdx_id_for_license_expression(CustomLicense, document_namespace, license_element_counts),
                "blank",
                creation_info,
            )
            _add_license(license, payload, license_element_counts)
            return license
    raise ValueError(f"Unsupported license expression type: {type(license_expression)}")


def bump_license_exception(
    license_exception: LicenseSymbol,
    extracted_licensing_info: List[ExtractedLicensingInfo],
    document_namespace: str,
    creation_info: CreationInfo,
    payload: Payload,
    license_element_counts: (
        dict[type, int] | None
    ) = None,  # do not use this argument unless already inside a bump_license_expression
) -> LicenseAddition:
    if not license_element_counts:
        license_element_counts = _get_count_of_license_expression_types(LICENSE_EXPRESSION_TYPES, payload)

    if not spdx_licensing.validate(license_exception).invalid_symbols:
        license = ListedLicenseException(
            _get_spdx_id_for_license_expression(ListedLicenseException, document_namespace, license_element_counts),
            license_exception.key,
            creation_info,
        )
        _add_license(license, payload, license_element_counts)
        return license
    else:
        for licensing_info in extracted_licensing_info:
            if licensing_info.license_id == license_exception.key:
                # the fields are optional in ExtractedLicensingInfo, to prevent type errors we use a type conversion
                # to str as a quick fix
                license = CustomLicenseAddition(
                    _get_spdx_id_for_license_expression(
                        CustomLicenseAddition, document_namespace, license_element_counts
                    ),
                    str(licensing_info.extracted_text),
                    creation_info,
                )
                _add_license(license, payload, license_element_counts)
                return license

        license = CustomLicenseAddition(
            _get_spdx_id_for_license_expression(CustomLicenseAddition, document_namespace, license_element_counts),
            license_exception.key,
            creation_info,
        )
        _add_license(license, payload, license_element_counts)
        return license
