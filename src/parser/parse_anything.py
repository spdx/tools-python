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
from src.formats import file_name_to_format, FileFormat
from src.parser.json.json_parser import JsonParser


def parse_file(file_name: str):
    input_format = file_name_to_format(file_name)
    if input_format == FileFormat.RDF:
        raise NotImplementedError("Currently, the rdf parser is not implemented")
    elif input_format == FileFormat.TAG_VALUE:
        raise NotImplementedError("Currently, the tag-value parser is not implemented")
    elif input_format == FileFormat.JSON:
        return JsonParser().parse(file_name)
    elif input_format == FileFormat.XML:
        raise NotImplementedError("Currently, the xml parser is not implemented")
    elif input_format == FileFormat.YAML:
        raise NotImplementedError("Currently, the yaml parser is not implemented")
