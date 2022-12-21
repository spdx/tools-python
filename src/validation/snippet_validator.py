from typing import List

from src.model.document import Document
from src.model.snippet import Snippet
from src.validation.license_expression_validator import LicenseExpressionValidator
from src.validation.spdx_id_validators import validate_spdx_id
from src.validation.validation_message import ValidationMessage, ValidationContext, SpdxElementType


class SnippetValidator:
    spdx_version: str
    document: Document
    license_expression_validator: LicenseExpressionValidator

    def __init__(self, spdx_version: str, document: Document):
        self.spdx_version = spdx_version
        self.document = document
        self.license_expression_validator = LicenseExpressionValidator(spdx_version)

    def validate_snippets(self, snippets: List[Snippet]) -> List[ValidationMessage]:
        validation_messages = []
        for snippet in snippets:
            validation_messages.extend(self.validate_snippet(snippet))

        return validation_messages

    def validate_snippet(self, snippet: Snippet) -> List[ValidationMessage]:
        validation_messages = []
        context = ValidationContext(spdx_id=snippet.spdx_id, element_type=SpdxElementType.SNIPPET, full_element=snippet)

        messages: List[str] = validate_spdx_id(snippet.spdx_id, self.document)
        for message in messages:
            validation_messages.append(ValidationMessage(message, context))

        messages: List[str] = validate_spdx_id(snippet.file_spdx_id, self.document, check_files=True)
        for message in messages:
            validation_messages.append(ValidationMessage(message, context))

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

        validation_messages.extend(
            self.license_expression_validator.validate_license_expression(snippet.concluded_license)
        )

        validation_messages.extend(
            self.license_expression_validator.validate_license_expressions(snippet.license_info_in_snippet)
        )

        return validation_messages
