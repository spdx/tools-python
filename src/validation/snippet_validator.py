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
        error_messages = []
        for snippet in snippets:
            error_messages.extend(self.validate_snippet(snippet))

        return error_messages

    def validate_snippet(self, snippet: Snippet) -> List[ValidationMessage]:
        pass
