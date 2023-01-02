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
from src.parser.error import SPDXParsingError
from src.parser.json.json_parser import JsonParser


def parse_file(file_name: str):
    if file_name.endswith(".rdf") or file_name.endswith(".rdf.xml"):
        raise NotImplementedError("Currently, the rdf parser is not implemented")
    elif file_name.endswith(".tag") or file_name.endswith(".spdx"):
        raise NotImplementedError("Currently, the tag-value parser is not implemented")
    elif file_name.endswith(".json"):
        return JsonParser().parse(file_name)
    elif file_name.endswith(".xml"):
        raise NotImplementedError("Currently, the xml parser is not implemented")
    elif file_name.endswith(".yaml") or file_name.endswith(".yml"):
        raise NotImplementedError("Currently, the yaml parser is not implemented")
    else:
        raise SPDXParsingError(["Unsupported file type: " + str(file_name)])
