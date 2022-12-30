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

from src.jsonschema.document_converter import DocumentConverter
from src.model.document import Document


def write_document(document: Document, file_name: str, converter: DocumentConverter = None):
    if converter is None:
        converter = DocumentConverter()
    document_dict = converter.convert(document)
    with open(file_name, "w") as out:
        json.dump(document_dict, out, indent=4)
