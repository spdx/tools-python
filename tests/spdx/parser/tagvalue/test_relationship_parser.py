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

from spdx.model.relationship import RelationshipType, Relationship
from spdx.model.spdx_no_assertion import SpdxNoAssertion
from spdx.model.spdx_none import SpdxNone
from spdx.parser.error import SPDXParsingError
from spdx.parser.tagvalue.parser import Parser
from tests.spdx.parser.tagvalue.test_creation_info_parser import DOCUMENT_STR


@pytest.mark.parametrize("relationship_str, expected_relationship",
                         [("\n".join(["Relationship: SPDXRef-DOCUMENT DESCRIBES SPDXRef-File",
                                      "RelationshipComment: This is a comment."]),
                           Relationship("SPDXRef-DOCUMENT", RelationshipType.DESCRIBES,
                                        "SPDXRef-File", "This is a comment.")),
                          ("Relationship: SPDXRef-DOCUMENT PATCH_FOR NOASSERTION",
                           Relationship("SPDXRef-DOCUMENT", RelationshipType.PATCH_FOR,
                                        SpdxNoAssertion())),
                          ("Relationship: SPDXRef-CarolCompression DEPENDS_ON NONE",
                           Relationship("SPDXRef-CarolCompression", RelationshipType.DEPENDS_ON, SpdxNone())),
                          ("Relationship: DocumentRef-ExternalDocument:SPDXRef-Test DEPENDS_ON DocumentRef:AnotherRef",
                           Relationship("DocumentRef-ExternalDocument:SPDXRef-Test", RelationshipType.DEPENDS_ON,
                                        "DocumentRef:AnotherRef"))
                          ])
def test_parse_relationship(relationship_str, expected_relationship):
    parser = Parser()
    document = parser.parse("\n".join([DOCUMENT_STR, relationship_str]))
    assert document is not None
    assert len(document.relationships) == 1
    relationship = document.relationships[0]
    assert relationship == expected_relationship


@pytest.mark.parametrize("relationship_str, expected_message",
                         [("Relationship: spdx_id DESCRIBES",
                           ['Error while parsing Relationship: ["Relationship couldn\'t be split in '
                            'spdx_element_id, relationship_type and related_spdx_element. Line: 1"]']),
                          ("Relationship: spdx_id IS spdx_id",
                           ["Error while parsing Relationship: ['Invalid RelationshipType IS. Line: 1']"])])
def test_parse_invalid_relationship(relationship_str, expected_message):
    parser = Parser()
    with pytest.raises(SPDXParsingError) as err:
        parser.parse(relationship_str)

    assert err.value.get_messages() == expected_message
