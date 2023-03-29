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
from spdx.parser.rdf import rdf_parser


def test_rdf_parser_file_not_found():
    with pytest.raises(FileNotFoundError, match="No such file or directory") as err:
        wrong_file_path = os.path.join(os.path.dirname(__file__), 'hnjfkjsedhnflsiafg.json')
        rdf_parser.parse_from_file(wrong_file_path)


def test_rdf_parser_with_2_3_example():
    doc = rdf_parser.parse_from_file(
        os.path.join(os.path.dirname(__file__), "../../data/formats/SPDXRdfExample-v2.3.spdx.rdf.xml"))

    assert type(doc) == Document
    assert len(doc.snippets) == 1
    assert len(doc.files) == 5
    assert len(doc.annotations) == 5
    assert len(doc.packages) == 4
    assert len(doc.relationships) == 13
    assert len(doc.extracted_licensing_info) == 5
