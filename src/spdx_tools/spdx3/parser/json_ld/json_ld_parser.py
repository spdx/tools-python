# SPDX-FileCopyrightText: 2026-present SPDX contributors
# SPDX-License-Identifier: Apache-2.0
from spdx_python_model import v3_0_1 as spdx_3_0

from spdx_tools.spdx3.object_set import SpdxObjectSet
from spdx_tools.spdx.parser.error import SPDXParsingError


def parse_from_file(file_name: str, encoding: str = "utf-8") -> SpdxObjectSet:
    """Read a SPDX 3 JSON-LD file into a SHACLObjectSet (the in-memory representation
    provided by the spdx-python-model bindings)."""
    object_set = spdx_3_0.SHACLObjectSet()
    try:
        # The binding's deserializer reads from a binary stream.
        with open(file_name, "rb") as file:
            spdx_3_0.JSONLDDeserializer().read(file, object_set)
    except OSError as err:
        raise SPDXParsingError([f"Could not open file {file_name}: {err}"])
    except Exception as err:
        raise SPDXParsingError([f"Error while parsing {file_name}: {err}"])
    return object_set
