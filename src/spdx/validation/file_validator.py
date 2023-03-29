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

from typing import List, Optional

from spdx.model.checksum import ChecksumAlgorithm
from spdx.model.document import Document
from spdx.model.file import File
from spdx.validation.checksum_validator import validate_checksums
from spdx.validation.license_expression_validator import validate_license_expressions, validate_license_expression
from spdx.validation.spdx_id_validators import validate_spdx_id
from spdx.validation.validation_message import ValidationMessage, ValidationContext, SpdxElementType


def validate_files(files: List[File], spdx_version: str, document: Optional[Document] = None) -> List[
    ValidationMessage]:
    validation_messages = []
    if document:
        for file in files:
            validation_messages.extend(validate_file_within_document(file, spdx_version, document))
    else:
        for file in files:
            validation_messages.extend(validate_file(file, spdx_version))

    return validation_messages


def validate_file_within_document(file: File, spdx_version: str, document: Document) -> List[ValidationMessage]:
    validation_messages: List[ValidationMessage] = []
    context = ValidationContext(spdx_id=file.spdx_id, parent_id=document.creation_info.spdx_id,
                                element_type=SpdxElementType.FILE, full_element=file)

    for message in validate_spdx_id(file.spdx_id, document):
        validation_messages.append(ValidationMessage(message, context))

    validation_messages.extend(validate_license_expression(file.license_concluded, document, file.spdx_id))

    validation_messages.extend(validate_license_expressions(file.license_info_in_file, document, file.spdx_id))

    validation_messages.extend(validate_file(file, spdx_version, context))

    return validation_messages


def validate_file(file: File, spdx_version: str, context: Optional[ValidationContext] = None) -> List[
    ValidationMessage]:
    validation_messages = []
    if not context:
        context = ValidationContext(spdx_id=file.spdx_id, element_type=SpdxElementType.FILE, full_element=file)

    if file.name.startswith("/"):
        validation_messages.append(
            ValidationMessage(
                f'file name must not be an absolute path starting with "/", but is: {file.name}', context)
        )

    if ChecksumAlgorithm.SHA1 not in [checksum.algorithm for checksum in file.checksums]:
        validation_messages.append(
            ValidationMessage(
                f"checksums must contain a SHA1 algorithm checksum, but only contains: {[checksum.algorithm for checksum in file.checksums]}",
                context)
        )

    validation_messages.extend(validate_checksums(file.checksums, file.spdx_id, spdx_version))

    if spdx_version == "SPDX-2.2":
        if file.license_concluded is None:
            validation_messages.append(
                ValidationMessage(f"license_concluded is mandatory in SPDX-2.2", context))
        if not file.license_info_in_file:
            validation_messages.append(
                ValidationMessage(f"license_info_in_file is mandatory in SPDX-2.2", context))
        if file.copyright_text is None:
            validation_messages.append(
                ValidationMessage(f"copyright_text is mandatory in SPDX-2.2", context))

    return validation_messages
