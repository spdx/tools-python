# SPDX-FileCopyrightText: 2026-present SPDX contributors
# SPDX-License-Identifier: Apache-2.0
from enum import Enum, auto

from spdx_tools.spdx.parser.error import SPDXParsingError


class FileFormat(Enum):
    JSON_LD = auto()


def file_name_to_format(file_name: str) -> FileFormat:
    # SPDX 3.0 currently defines a single serialization: JSON-LD.
    # Common extensions are "spdx3.json", ".json" and ".jsonld".
    # See:
    # https://github.com/OpenChain-Project/Telco-WG/blob/main/OpenChain-Telco-SBOM-Guide_1.2_DRAFT_EN.md
    # https://www.iana.org/assignments/media-types/application/spdx3+json
    if file_name.endswith(".json") or file_name.endswith(".jsonld"):
        return FileFormat.JSON_LD
    else:
        raise SPDXParsingError(["Unsupported SPDX 3 file type: " + str(file_name)])
