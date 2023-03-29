# Copyright (c) 2022 spdx contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from enum import Enum, auto

from spdx.parser.error import SPDXParsingError


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
