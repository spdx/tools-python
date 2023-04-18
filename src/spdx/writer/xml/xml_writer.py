# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from typing import List

import xmltodict

from spdx.document_utils import create_document_without_duplicates
from spdx.jsonschema.document_converter import DocumentConverter
from spdx.model.document import Document
from spdx.validation.document_validator import validate_full_spdx_document
from spdx.validation.validation_message import ValidationMessage


def write_document_to_file(
    document: Document,
    file_name: str,
    validate: bool = True,
    converter: DocumentConverter = None,
    drop_duplicates: bool = True,
):
    """
    Serializes the provided document to XML and writes it to a file with the provided name. Unless validate is set
    to False, validates the document before serialization. Unless a DocumentConverter instance is provided,
    a new one is created.
    """
    if validate:
        validation_messages: List[ValidationMessage] = validate_full_spdx_document(document)
        if validation_messages:
            raise ValueError(f"Document is not valid. The following errors were detected: {validation_messages}")
    if drop_duplicates:
        document = create_document_without_duplicates(document)

    if converter is None:
        converter = DocumentConverter()
    document_dict = {"Document": converter.convert(document)}
    with open(file_name, "w") as out:
        xmltodict.unparse(document_dict, out, encoding="utf-8", pretty=True)
