# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import json
from typing import List

from spdx.jsonschema.document_converter import DocumentConverter
from spdx.model.document import Document
from spdx.validation.document_validator import validate_full_spdx_document
from spdx.validation.validation_message import ValidationMessage


def write_document(document: Document, file_name: str, validate: bool = True, converter: DocumentConverter = None):
    """
    Serializes the provided document to json and writes it to a file with the provided name. Unless validate is set
    to False, validates the document before serialization. Unless a DocumentConverter instance is provided,
    a new one is created.
    """
    if validate:
        validation_messages: List[ValidationMessage] = validate_full_spdx_document(document)
        if validation_messages:
            raise ValueError(f"Document is not valid. The following errors were detected: {validation_messages}")
    if converter is None:
        converter = DocumentConverter()
    document_dict = converter.convert(document)
    with open(file_name, "w") as out:
        json.dump(document_dict, out, indent=4)
