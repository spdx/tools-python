#  SPDX-FileCopyrightText: 2023 spdx contributors
#
#  SPDX-License-Identifier: Apache-2.0
from os import path

from spdx_tools.spdx.model import Document
from spdx_tools.spdx3.payload import Payload
from spdx_tools.spdx3.writer.json_ld.json_ld_writer import write_payload
from spdx_tools.spdx3.bump_from_spdx2.spdx_document import bump_spdx_document
from spdx_tools.spdx.parser.parse_anything import parse_file

# This example demonstrates how to load an existing SPDX2 file and convert it to the SPDX3 format

# Provide a path to the input file
input_path = path.join(path.dirname(__file__), "..", "tests", "spdx", "data", "SPDXLite.spdx")
# Parse the original SPDX2 input file
spdx2_document: Document = parse_file(input_path)
# Convert original document to an SPDX3 payload
spdx3_payload: Payload = bump_spdx_document(spdx2_document)
# Write SPDX3 payload in json-ld format
write_payload(spdx3_payload, "spdx2_to_3")
