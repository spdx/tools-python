#  SPDX-FileCopyrightText: 2023 spdx contributors
#
#  SPDX-License-Identifier: Apache-2.0
from os import path

from spdx_tools.spdx.model import Document
from spdx_tools.spdx.writer.write_anything import write_file
from spdx_tools.spdx.parser.parse_anything import parse_file

# This example demonstrates how to load an existing SPDX2 file and convert it to a different SPDX2 format

# Provide a path to the input file in the originating format
input_path = path.join(path.dirname(__file__), "..", "tests", "spdx", "data", "SPDXLite.spdx")
# Parse the original input file (format is deduced automatically from the file extension)
document: Document = parse_file(input_path)
# Write to a different file format (e.g. XML, format is deduced automatically from the file extension)
write_file(document, "converted_format.xml")
