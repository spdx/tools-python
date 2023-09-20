# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import json

from beartype.typing import IO

from spdx_tools.spdx.jsonschema.document_converter import DocumentConverter
from spdx_tools.spdx.model import Document
from spdx_tools.spdx.writer.write_utils import convert, validate_and_deduplicate


def write_document_to_stream(
    document: Document,
    stream: IO[str],
    validate: bool = True,
    converter: DocumentConverter = None,
    drop_duplicates: bool = True,
):
    """
    Serializes the provided document to json and writes it to a file with the provided name. Unless validate is set
    to False, validates the document before serialization. Unless a DocumentConverter instance is provided,
    a new one is created.
    """
    document = validate_and_deduplicate(document, validate, drop_duplicates)
    document_dict = convert(document, converter)
    json.dump(document_dict, stream, indent=4)


def write_document_to_file(
    document: Document,
    file_name: str,
    validate: bool = True,
    converter: DocumentConverter = None,
    drop_duplicates: bool = True,
):
    with open(file_name, "w", encoding="utf-8") as out:
        write_document_to_stream(document, out, validate, converter, drop_duplicates)
