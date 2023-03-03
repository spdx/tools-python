# Copyright (c) 2022 spdx contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import List, Optional, Union

from license_expression import LicenseExpression, get_spdx_licensing, ExpressionError, ExpressionParseError
from spdx.model.document import Document

from spdx.model.spdx_no_assertion import SpdxNoAssertion
from spdx.model.spdx_none import SpdxNone
from spdx.validation.validation_message import ValidationMessage, ValidationContext, SpdxElementType


def validate_license_expressions(
    license_expressions: List[Union[LicenseExpression, SpdxNoAssertion, SpdxNone]],
        document: Document, parent_id: str) -> List[ValidationMessage]:
    context = ValidationContext(parent_id=parent_id, element_type=SpdxElementType.LICENSE_EXPRESSION,
                                full_element=license_expressions)
    validation_messages = []

    for license_expression in license_expressions:
        validation_messages.extend(validate_license_expression(license_expression, document, parent_id, context))

    return validation_messages


def validate_license_expression(
    license_expression: Optional[Union[LicenseExpression, SpdxNoAssertion, SpdxNone]], document: Document,
        parent_id: str, context: ValidationContext = None) -> List[ValidationMessage]:
    if license_expression in [SpdxNoAssertion(), SpdxNone(), None]:
        return []

    if not context:
        context = ValidationContext(parent_id=parent_id, element_type=SpdxElementType.LICENSE_EXPRESSION,
                                    full_element=license_expression)

    validation_messages = []
    license_ref_ids: List[str] = [license_ref.license_id for license_ref in document.extracted_licensing_info]

    for non_spdx_token in get_spdx_licensing().validate(license_expression).invalid_symbols:
        if non_spdx_token not in license_ref_ids:
            validation_messages.append(
                ValidationMessage(
                    f"Unrecognized license reference: {non_spdx_token}. license_expression must only use IDs from the license list or extracted licensing info, but is: {license_expression}",
                    context)
            )

    try:
        get_spdx_licensing().parse(str(license_expression), validate=True, strict=True)
    except ExpressionParseError as err:
        # This error is raised when an exception symbol is used as a license symbol and vice versa.
        # So far, it only catches the first such error in the provided string.
        validation_messages.append(
            ValidationMessage(
                f"{err}. for license_expression: {license_expression}",
                context)
        )
    except ExpressionError:
        # This error is raised for invalid symbols within the license_expression, but it provides only a string of these.
        # On the other hand, get_spdx_licensing().validate() gives an actual list of invalid symbols, so this is handled above.
        pass

    return validation_messages
