# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from enum import Enum, auto

from spdx_tools.spdx.parser.error import SPDXParsingError


class FileFormat(Enum):
    JSON = auto()
    YAML = auto()
    XML = auto()
    TAG_VALUE = auto()
    RDF_XML = auto()


def file_name_to_format(file_name: str) -> FileFormat:
    if file_name.endswith(".rdf") or file_name.endswith(".rdf.xml"):
        return FileFormat.RDF_XML
    elif file_name.endswith(".tag") or file_name.endswith(".spdx"):
        return FileFormat.TAG_VALUE
    elif file_name.endswith(".json"):
        return FileFormat.JSON
    elif file_name.endswith(".xml"):
        return FileFormat.XML
    elif file_name.endswith(".yaml") or file_name.endswith(".yml"):
        return FileFormat.YAML
    else:
        raise SPDXParsingError(["Unsupported SPDX file type: " + str(file_name)])
