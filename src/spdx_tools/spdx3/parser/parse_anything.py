# SPDX-FileCopyrightText: 2026-present SPDX contributors
# SPDX-License-Identifier: Apache-2.0
from spdx_tools.spdx3.formats import FileFormat, file_name_to_format
from spdx_tools.spdx3.object_set import SpdxObjectSet
from spdx_tools.spdx3.parser.json_ld import json_ld_parser
from spdx_tools.spdx.parser.error import SPDXParsingError


def parse_file(file_name: str, encoding: str = "utf-8") -> SpdxObjectSet:
    """Parse a SPDX 3 file into a SHACLObjectSet, dispatching on the file format.

    SPDX 3.0 currently defines a single serialization (JSON-LD); the dispatch is
    kept to mirror the SPDX 2 ``parse_file`` API and to ease adding formats later.
    """
    input_format = file_name_to_format(file_name)
    if input_format == FileFormat.JSON_LD:
        return json_ld_parser.parse_from_file(file_name, encoding)
    raise SPDXParsingError([f"Unsupported SPDX 3 file format: {input_format}"])
