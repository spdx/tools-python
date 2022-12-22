from typing import List

from src.model.document import Document
from src.model.snippet import Snippet
from src.validation.license_expression_validator import validate_license_expression, \
    validate_license_expressions
from src.validation.spdx_id_validators import validate_spdx_id
from src.validation.validation_message import ValidationMessage, ValidationContext, SpdxElementType


def validate_snippets(snippets: List[Snippet], document: Document) -> List[ValidationMessage]:
    validation_messages = []
    for snippet in snippets:
        validation_messages.extend(validate_snippet_within_document(snippet, document))

    return validation_messages


def validate_snippet_within_document(snippet: Snippet, document: Document) -> List[ValidationMessage]:
    validation_messages: List[ValidationMessage] = []
    context = ValidationContext(spdx_id=snippet.spdx_id, element_type=SpdxElementType.SNIPPET, full_element=snippet)

    messages: List[str] = validate_spdx_id(snippet.spdx_id, document)
    for message in messages:
        validation_messages.append(ValidationMessage(message, context))

    messages: List[str] = validate_spdx_id(snippet.file_spdx_id, document, check_files=True)
    for message in messages:
        validation_messages.append(ValidationMessage(message, context))

    validation_messages.extend(validate_snippet(snippet, context))

    return validation_messages


def validate_snippet(snippet: Snippet, context: ValidationContext) -> List[ValidationMessage]:
    validation_messages = []

    if snippet.byte_range[0] < 1:
        validation_messages.append(
            ValidationMessage(
                f"byte_range values must be greater than or equal to 1, but is: {snippet.byte_range}",
                context)
        )

    if snippet.byte_range[0] > snippet.byte_range[1]:
        validation_messages.append(
            ValidationMessage(
                f"the first value of byte_range must be less than or equal to the second, but is: {snippet.byte_range}",
                context)
        )

    if snippet.line_range:
        if snippet.line_range[0] < 1:
            validation_messages.append(
                ValidationMessage(
                    f"line_range values must be greater than or equal to 1, but is: {snippet.line_range}",
                    context)
            )

        if snippet.line_range[0] > snippet.line_range[1]:
            validation_messages.append(
                ValidationMessage(
                    f"the first value of line_range must be less than or equal to the second, but is: {snippet.line_range}",
                    context)
            )

    validation_messages.extend(validate_license_expression(snippet.concluded_license))

    validation_messages.extend(validate_license_expressions(snippet.license_info_in_snippet))

    return validation_messages
