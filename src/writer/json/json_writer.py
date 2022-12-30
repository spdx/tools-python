#  Copyright (c) 2022 spdx contributors
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#      http://www.apache.org/licenses/LICENSE-2.0
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
import json
from typing import List

from src.jsonschema.document_converter import DocumentConverter
from src.model.document import Document
from src.validation.document_validator import validate_full_spdx_document
from src.validation.validation_message import ValidationMessage


def write_document(document: Document, file_name: str, validate: bool = True, converter: DocumentConverter = None):
    if validate:
        validation_messages: List[ValidationMessage] = validate_full_spdx_document(document,
                                                                                   document.creation_info.spdx_version)
        if validation_messages:
            raise ValueError(f"Document is not valid. The following errors were detected: {validation_messages}")
    if converter is None:
        converter = DocumentConverter()
    document_dict = converter.convert(document)
    with open(file_name, "w") as out:
        json.dump(document_dict, out, indent=4)
