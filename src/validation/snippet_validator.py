from typing import List

from src.model.snippet import Snippet
from src.validation.checksum_validator import ChecksumValidator
from src.validation.validation_message import ValidationMessage
from src.validation.license_expression_validator import LicenseExpressionValidator


class SnippetValidator:
    spdx_version: str
    checksum_validator: ChecksumValidator
    license_expression_validator: LicenseExpressionValidator

    def __init__(self, spdx_version):
        self.spdx_version = spdx_version
        self.checksum_validator = ChecksumValidator(spdx_version)
        self.license_expression_validator = LicenseExpressionValidator(spdx_version)

    def validate_snippets(self, snippets: List[Snippet]) -> List[ValidationMessage]:
        validation_messages = []
        for snippet in snippets:
            validation_messages.extend(self.validate_snippet(snippet))

        return validation_messages

    def validate_snippet(self, snippet: Snippet) -> List[ValidationMessage]:
        validation_messages = []

        # TODO: check that file_id is external or present in the document

        validation_messages.append(
            self.license_expression_validator.validate_license_expression(snippet.concluded_license)
        )

        validation_messages.extend(
            self.license_expression_validator.validate_license_expressions(snippet.license_info_in_snippet)
        )

        return validation_messages
