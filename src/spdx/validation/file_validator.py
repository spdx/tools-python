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


def validate_files(files: List[File], document: Optional[Document] = None) -> List[ValidationMessage]:
    validation_messages = []
    if document:
        for file in files:
            validation_messages.extend(validate_file_within_document(file, document))
    else:
        for file in files:
            validation_messages.extend(validate_file(file))

    return validation_messages


def validate_file_within_document(file: File, document: Document) -> List[ValidationMessage]:
    validation_messages: List[ValidationMessage] = []
    context = ValidationContext(spdx_id=file.spdx_id, parent_id=document.creation_info.spdx_id,
                                element_type=SpdxElementType.FILE, full_element=file)

    for message in validate_spdx_id(file.spdx_id, document):
        validation_messages.append(ValidationMessage(message, context))

    validation_messages.extend(validate_file(file, context))

    return validation_messages


def validate_file(file: File, context: Optional[ValidationContext] = None) -> List[ValidationMessage]:
    validation_messages = []
    if not context:
        context = ValidationContext(spdx_id=file.spdx_id, element_type=SpdxElementType.FILE, full_element=file)

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
