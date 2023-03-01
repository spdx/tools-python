# Copyright (c) 2014 Ahmed H. Ismail
# Copyright (c) 2023 spdx contributors
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
from spdx.parser.error import SPDXParsingError
from spdx.parser.tagvalue.parser.tagvalue import Parser


def test_unknown_str():
    parser = Parser()
    unknown_tag_str = 'UnknownTag: This is an example for an unknown tag.'

    with pytest.raises(SPDXParsingError, match="Unknown tag"):
        parser.parse(unknown_tag_str)


def test_parse_file():
    parser = Parser()
    fn = os.path.join(os.path.dirname(__file__), "../../data/formats/SPDXTagExample-v2.3.spdx")

    with open(fn) as f:
        data = f.read()
        doc = parser.parse(data)
    assert type(doc) == Document
    assert len(doc.annotations) == 5
    assert len(doc.files) == 5
    assert len(doc.packages) == 4
    assert len(doc.snippets) == 1
    assert len(doc.relationships) == 13
    assert len(doc.extracted_licensing_info) == 5
