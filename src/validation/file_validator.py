from typing import List

from src.model.file import File
from src.validation.checksum_validator import ChecksumValidator
from src.validation.validation_message import ValidationMessage
from src.validation.license_expression_validator import LicenseExpressionValidator


class FileValidator:
    spdx_version: str
    license_expression_validator: LicenseExpressionValidator

    def __init__(self, spdx_version):
        self.spdx_version = spdx_version
        self.license_expression_validator = LicenseExpressionValidator(spdx_version)

    def validate_files(self, files: List[File]) -> List[ValidationMessage]:
        validation_messages = []
        for file in files:
            validation_messages.extend(self.validate_file(file))

        return validation_messages

    def validate_file(self, file: File) -> List[ValidationMessage]:
        validation_messages = []
        checksum_validator = ChecksumValidator(self.spdx_version, file.spdx_id)

        validation_messages.extend(
            checksum_validator.validate_checksums(file.checksums)
        )

        validation_messages.append(
            self.license_expression_validator.validate_license_expression(file.concluded_license)
        )

        validation_messages.extend(
            self.license_expression_validator.validate_license_expressions(file.license_info_in_file)
        )

        return validation_messages

