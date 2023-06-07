# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0

from beartype.typing import List, Optional, Union
from license_expression import ExpressionError, ExpressionParseError, LicenseExpression, get_spdx_licensing

from spdx_tools.spdx.model import Document, SpdxNoAssertion, SpdxNone
from spdx_tools.spdx.validation.validation_message import SpdxElementType, ValidationContext, ValidationMessage


def validate_license_expressions(
    license_expressions: List[Union[LicenseExpression, SpdxNoAssertion, SpdxNone]], document: Document, parent_id: str
) -> List[ValidationMessage]:
    context = ValidationContext(
        parent_id=parent_id, element_type=SpdxElementType.LICENSE_EXPRESSION, full_element=license_expressions
    )
    validation_messages = []

    for license_expression in license_expressions:
        validation_messages.extend(validate_license_expression(license_expression, document, parent_id, context))

    return validation_messages


def validate_license_expression(
    license_expression: Optional[Union[LicenseExpression, SpdxNoAssertion, SpdxNone]],
    document: Document,
    parent_id: str,
    context: ValidationContext = None,
) -> List[ValidationMessage]:
    if license_expression in [SpdxNoAssertion(), SpdxNone(), None]:
        return []

    if not context:
        context = ValidationContext(
            parent_id=parent_id, element_type=SpdxElementType.LICENSE_EXPRESSION, full_element=license_expression
        )

    validation_messages = []
    license_ref_ids: List[str] = [license_ref.license_id for license_ref in document.extracted_licensing_info]

    for non_spdx_token in get_spdx_licensing().validate(license_expression).invalid_symbols:
        if non_spdx_token not in license_ref_ids:
            validation_messages.append(
                ValidationMessage(
                    f"Unrecognized license reference: {non_spdx_token}. license_expression must only use IDs from the "
                    f"license list or extracted licensing info, but is: {license_expression}",
                    context,
                )
            )

    try:
        get_spdx_licensing().parse(str(license_expression), validate=True, strict=True)
    except ExpressionParseError as err:
        # This error is raised when an exception symbol is used as a license symbol and vice versa.
        # So far, it only catches the first such error in the provided string.
        validation_messages.append(ValidationMessage(f"{err}. for license_expression: {license_expression}", context))
    except ExpressionError:
        # This error is raised for invalid symbols within the license_expression, but it provides only a string of
        # these. On the other hand, get_spdx_licensing().validate() gives an actual list of invalid symbols, so this is
        # handled above.
        pass

    return validation_messages
