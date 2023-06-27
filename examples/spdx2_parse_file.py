#  SPDX-FileCopyrightText: 2023 spdx contributors
#
#  SPDX-License-Identifier: Apache-2.0
import logging
from os import path

from spdx_tools.spdx.model.document import Document
from spdx_tools.spdx.parser.error import SPDXParsingError
from spdx_tools.spdx.parser.parse_anything import parse_file

# This example demonstrates how to parse an existing spdx file.

# Provide a path to the input file
input_path = path.join(path.dirname(__file__), "..", "tests", "spdx", "data", "SPDXLite.spdx")
try:
    # Try to parse the input file. If successful, returns a Document, otherwise raises an SPDXParsingError
    document: Document = parse_file(input_path)
except SPDXParsingError:
    logging.exception("Failed to parse spdx file")

# We can now access attributes from the parsed document
print(f"Parsed document name: {document.creation_info.name}")
creators_as_str = ", ".join([creator.to_serialized_string() for creator in document.creation_info.creators])
print(f"Created on {document.creation_info.created} by {creators_as_str}")
