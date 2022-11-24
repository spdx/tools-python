from typing import List

from src.model.checksum import ChecksumAlgorithm
from src.model.document import Document
from src.model.file import File
from src.validation.checksum_validator import ChecksumValidator
from src.validation.spdx_id_validation import is_valid_spdx_id, validate_spdx_id
from src.validation.validation_message import ValidationMessage, ValidationContext, SpdxElementType
from src.validation.license_expression_validator import LicenseExpressionValidator


class FileValidator:
    spdx_version: str
    document: Document
    license_expression_validator: LicenseExpressionValidator

    def __init__(self, spdx_version: str, document: Document):
        self.spdx_version = spdx_version
        self.document = document
        self.license_expression_validator = LicenseExpressionValidator(spdx_version)

    def validate_files(self, files: List[File]) -> List[ValidationMessage]:
        validation_messages = []
        for file in files:
            validation_messages.extend(self.validate_file(file))

        return validation_messages

    def validate_file(self, file: File) -> List[ValidationMessage]:
        validation_messages = []
        checksum_validator = ChecksumValidator(self.spdx_version, file.spdx_id)
        context = ValidationContext(spdx_id=file.spdx_id, element_type=SpdxElementType.FILE, full_element=file)

        for message in validate_spdx_id(file.spdx_id, self.document):
            validation_messages.append(ValidationMessage(message, context))

        if not file.name.startswith("./"):
            validation_messages.append(
                ValidationMessage(
                    f'file name must be a relative path to the file, starting with "./", but is: {file.name}',
                    context)
            )

        if ChecksumAlgorithm.SHA1 not in [checksum.algorithm for checksum in file.checksums]:
            validation_messages.append(
                ValidationMessage(
                    f'checksums must contain a SHA1 algorithm checksum, but is: {file.checksums}',
                    context)
            )

        validation_messages.extend(
            checksum_validator.validate_checksums(file.checksums)
        )

        validation_messages.extend(
            self.license_expression_validator.validate_license_expression(file.concluded_license)
        )

        validation_messages.extend(
            self.license_expression_validator.validate_license_expressions(file.license_info_in_file)
        )

        return validation_messages
