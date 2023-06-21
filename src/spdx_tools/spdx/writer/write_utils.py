# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from beartype.typing import List

from spdx_tools.spdx.document_utils import create_document_without_duplicates
from spdx_tools.spdx.jsonschema.document_converter import DocumentConverter
from spdx_tools.spdx.model import Document
from spdx_tools.spdx.validation.document_validator import validate_full_spdx_document
from spdx_tools.spdx.validation.validation_message import ValidationMessage


def validate_and_deduplicate(document: Document, validate: bool = True, drop_duplicates: bool = True) -> Document:
    if validate:
        validation_messages: List[ValidationMessage] = validate_full_spdx_document(document)
        if validation_messages:
            raise ValueError(f"Document is not valid. The following errors were detected: {validation_messages}")
    if drop_duplicates:
        document = create_document_without_duplicates(document)
    return document


def convert(document: Document, converter: DocumentConverter) -> dict:
    if converter is None:
        converter = DocumentConverter()
    return converter.convert(document)
