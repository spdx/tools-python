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
import pytest

from spdx.model.relationship import RelationshipType
from spdx.parser.error import SPDXParsingError
from spdx.parser.tagvalue.parser.tagvalue import Parser
from tests.spdx.parser.tagvalue.test_creation_info_parser import DOCUMENT_STR


@pytest.fixture
def parser():
    spdx_parser = Parser()
    spdx_parser.build()
    return spdx_parser


def test_relationship(parser):
    relationship_str = '\n'.join([
        'Relationship: SPDXRef-DOCUMENT DESCRIBES SPDXRef-File',
        'RelationshipComment: This is a comment.'])

    document = parser.parse("\n".join([DOCUMENT_STR, relationship_str]))
    assert document is not None
    relationship = document.relationships[0]
    assert relationship.relationship_type == RelationshipType.DESCRIBES
    assert relationship.related_spdx_element_id == "SPDXRef-File"
    assert relationship.spdx_element_id == "SPDXRef-DOCUMENT"
    assert relationship.comment == "This is a comment."


@pytest.mark.parametrize("relationship_str, expected_message",
                         [("Relationship: spdx_id DESCRIBES", "Relationship couldn't be split"),
                          ("Relationship: spdx_id IS spdx_id", "Invalid RelationshipType IS. Line: 1")])
def test_falsy_relationship(parser, relationship_str, expected_message):
    with pytest.raises(SPDXParsingError, match=expected_message):
        parser.parse(relationship_str)
