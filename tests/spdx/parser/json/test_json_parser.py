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

import os
import pytest

from spdx.model.document import Document
from spdx.parser.json import json_parser

def test_parse_json_file_not_found():
    with pytest.raises(FileNotFoundError) as err:
        wrong_file_path = os.path.join(os.path.dirname(__file__), 'hnjfkjsedhnflsiafg.json')
        json_parser.parse_from_file(wrong_file_path)

    assert err.value.args[1] == "No such file or directory"


def test_parse_json_with_2_3_example():
    doc = json_parser.parse_from_file(os.path.join(os.path.dirname(__file__),
                                                   "../../data/formats/SPDXJSONExample-v2.3.spdx.json"))
    assert type(doc) == Document
    assert len(doc.annotations) == 5
    assert len(doc.files) == 5
    assert len(doc.packages) == 4
    assert len(doc.snippets) ==  1
    assert len(doc.relationships) == 13
    assert len(doc.extracted_licensing_info) == 5

def test_parse_json_with_2_2_example():
    doc = json_parser.parse_from_file(os.path.join(os.path.dirname(__file__),
                                                   "../../data/formats/SPDXJSONExample-v2.2.spdx.json"))
    assert type(doc) == Document
    assert len(doc.annotations) == 5
    assert len(doc.files) == 4
    assert len(doc.packages) == 4
    assert len(doc.snippets) ==  1
    assert len(doc.relationships) == 11
    assert len(doc.extracted_licensing_info) == 5

