from typing import List

from src.model.file import File
from src.validation.checksum_validator import ChecksumValidator
from src.validation.validation_message import ValidationMessage
from src.validation.license_expression_validator import LicenseExpressionValidator


class FileValidator:
    spdx_version: str
    checksum_validator: ChecksumValidator
    license_expression_validator: LicenseExpressionValidator

    def __init__(self, spdx_version):
        self.spdx_version = spdx_version
        self.checksum_validator = ChecksumValidator(spdx_version)
        self.license_expression_validator = LicenseExpressionValidator(spdx_version)

    def validate_files(self, files: List[File]) -> List[ValidationMessage]:
        error_messages = []
        for file in files:
            error_messages.extend(self.validate_file(file))

        return error_messages

    def validate_file(self, file: File) -> List[ValidationMessage]:
        pass
