# SPDX-License-Identifier: Apache-2.0
# Copyright (c) spdx contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import logging

from spdx_tools.spdx.formats import FileFormat, file_name_to_format
from spdx_tools.spdx.parser.json import json_parser
from spdx_tools.spdx.parser.rdf import rdf_parser
from spdx_tools.spdx.parser.tagvalue import tagvalue_parser
from spdx_tools.spdx.parser.xml import xml_parser
from spdx_tools.spdx.parser.yaml import yaml_parser


def parse_file(file_name: str, encoding: str = "utf-8"):
    if encoding != "utf-8":
        logging.warning(
            "It's recommended to use the UTF-8 encoding for any SPDX file. Consider changing the encoding of the file."
        )

    input_format = file_name_to_format(file_name)
    if input_format == FileFormat.RDF_XML:
        return rdf_parser.parse_from_file(file_name, encoding)
    elif input_format == FileFormat.TAG_VALUE:
        return tagvalue_parser.parse_from_file(file_name, encoding)
    elif input_format == FileFormat.JSON:
        return json_parser.parse_from_file(file_name, encoding)
    elif input_format == FileFormat.XML:
        return xml_parser.parse_from_file(file_name, encoding)
    elif input_format == FileFormat.YAML:
        return yaml_parser.parse_from_file(file_name, encoding)
