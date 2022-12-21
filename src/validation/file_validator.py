from typing import List

from src.model.checksum import ChecksumAlgorithm
from src.model.document import Document
from src.model.file import File
from src.validation.checksum_validator import validate_checksums
from src.validation.license_expression_validator import validate_license_expressions, validate_license_expression
from src.validation.spdx_id_validators import validate_spdx_id
from src.validation.validation_message import ValidationMessage, ValidationContext, SpdxElementType


def validate_files(files: List[File], document: Document) -> List[ValidationMessage]:
    validation_messages = []
    for file in files:
        validation_messages.extend(validate_file(file, document))

    return validation_messages


def validate_file(file: File, document: Document) -> List[ValidationMessage]:
    validation_messages = []
    context = ValidationContext(spdx_id=file.spdx_id, element_type=SpdxElementType.FILE, full_element=file)

    for message in validate_spdx_id(file.spdx_id, document):
        validation_messages.append(ValidationMessage(message, context))

    if not file.name.startswith("./"):
        validation_messages.append(
            ValidationMessage(
                f'file name must be a relative path to the file, starting with "./", but is: {file.name}', context)
        )

    if ChecksumAlgorithm.SHA1 not in [checksum.algorithm for checksum in file.checksums]:
        validation_messages.append(
            ValidationMessage(
                f"checksums must contain a SHA1 algorithm checksum, but only contains: {[checksum.algorithm for checksum in file.checksums]}",
                context)
        )

    validation_messages.extend(validate_checksums(file.checksums, file.spdx_id))

    validation_messages.extend(validate_license_expression(file.concluded_license))

    validation_messages.extend(validate_license_expressions(file.license_info_in_file))

    return validation_messages
