# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0

from beartype.typing import List, Optional

from spdx_tools.spdx.model import Document, Snippet
from spdx_tools.spdx.validation.license_expression_validator import (
    validate_license_expression,
    validate_license_expressions,
)
from spdx_tools.spdx.validation.spdx_id_validators import validate_spdx_id
from spdx_tools.spdx.validation.validation_message import SpdxElementType, ValidationContext, ValidationMessage


def validate_snippets(
    snippets: List[Snippet], spdx_version: str, document: Optional[Document] = None
) -> List[ValidationMessage]:
    validation_messages = []
    if document:
        for snippet in snippets:
            validation_messages.extend(validate_snippet_within_document(snippet, spdx_version, document))
    else:
        for snippet in snippets:
            validation_messages.extend(validate_snippet(snippet, spdx_version))

    return validation_messages


def validate_snippet_within_document(
    snippet: Snippet, spdx_version: str, document: Document
) -> List[ValidationMessage]:
    validation_messages: List[ValidationMessage] = []
    context = ValidationContext(
        spdx_id=snippet.spdx_id,
        parent_id=document.creation_info.spdx_id,
        element_type=SpdxElementType.SNIPPET,
        full_element=snippet,
    )

    messages: List[str] = validate_spdx_id(snippet.spdx_id, document)
    for message in messages:
        validation_messages.append(ValidationMessage(message, context))

    messages: List[str] = validate_spdx_id(snippet.file_spdx_id, document, check_files=True)
    for message in messages:
        validation_messages.append(ValidationMessage(message, context))

    validation_messages.extend(validate_license_expression(snippet.license_concluded, document, snippet.spdx_id))

    validation_messages.extend(
        validate_license_expressions(snippet.license_info_in_snippet, document, snippet.spdx_id)
    )

    validation_messages.extend(validate_snippet(snippet, spdx_version, context))

    return validation_messages


def validate_snippet(
    snippet: Snippet, spdx_version: str, context: Optional[ValidationContext] = None
) -> List[ValidationMessage]:
    validation_messages = []
    if not context:
        context = ValidationContext(
            spdx_id=snippet.spdx_id, element_type=SpdxElementType.SNIPPET, full_element=snippet
        )

    if snippet.byte_range[0] < 1:
        validation_messages.append(
            ValidationMessage(
                f"byte_range values must be greater than or equal to 1, but is: {snippet.byte_range}", context
            )
        )

    if snippet.byte_range[0] > snippet.byte_range[1]:
        validation_messages.append(
            ValidationMessage(
                f"the first value of byte_range must be less than or equal to the second, but is: "
                f"{snippet.byte_range}",
                context,
            )
        )

    if snippet.line_range:
        if snippet.line_range[0] < 1:
            validation_messages.append(
                ValidationMessage(
                    f"line_range values must be greater than or equal to 1, but is: {snippet.line_range}", context
                )
            )

        if snippet.line_range[0] > snippet.line_range[1]:
            validation_messages.append(
                ValidationMessage(
                    f"the first value of line_range must be less than or equal to the second, "
                    f"but is: {snippet.line_range}",
                    context,
                )
            )

    if spdx_version == "SPDX-2.2":
        if snippet.license_concluded is None:
            validation_messages.append(ValidationMessage("license_concluded is mandatory in SPDX-2.2", context))
        if snippet.copyright_text is None:
            validation_messages.append(ValidationMessage("copyright_text is mandatory in SPDX-2.2", context))

    return validation_messages
