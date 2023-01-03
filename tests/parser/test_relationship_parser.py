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
from unittest import TestCase

import pytest

from src.model.relationship import RelationshipType, Relationship
from src.model.spdx_no_assertion import SpdxNoAssertion
from src.parser.error import SPDXParsingError
from src.parser.jsonlikedict.relationship_parser import RelationshipParser


def test_parse_relationship():
    relationship_parser = RelationshipParser()

    relationship_dict = {
        "spdxElementId": "SPDXRef-DOCUMENT",
        "relationshipType": "CONTAINS",
        "relatedSpdxElement": "NOASSERTION",
        "comment": "Comment."
    }

    relationship = relationship_parser.parse_relationship(relationship_dict)

    assert relationship.relationship_type == RelationshipType.CONTAINS
    assert relationship.spdx_element_id == "SPDXRef-DOCUMENT"
    assert relationship.related_spdx_element_id == SpdxNoAssertion()
    assert relationship.comment == "Comment."


def test_parse_incomplete_relationship():
    relationship_parser = RelationshipParser()
    relationship_dict = {
        "spdxElementId": "SPDXRef-DOCUMENT",
        "relatedSpdxElement": "SPDXRef-Package",
        "comment": "Comment."
    }

    with pytest.raises(SPDXParsingError) as err:
        relationship_parser.parse_relationship(relationship_dict)

    TestCase().assertCountEqual(err.value.get_messages(), [
        "Error while constructing Relationship: ['SetterError Relationship: type of " 'argument "relationship_type" must be ' "src.model.relationship.RelationshipType; got NoneType instead: None']"])


def test_parse_relationship_type():
    relationship_parser = RelationshipParser()
    relationship_type_str = "DEPENDENCY_OF"

    relationship_type = relationship_parser.parse_relationship_type(relationship_type_str)
    assert relationship_type == RelationshipType.DEPENDENCY_OF


def test_parse_document_describes():
    relationship_parser = RelationshipParser()

    document_dict = {
        "SPDXID": "SPDXRef-DOCUMENT",
        "documentDescribes": ["SPDXRef-Package", "SPDXRef-File", "SPDXRef-Snippet"]
    }

    relationships = relationship_parser.parse_document_describes(doc_spdx_id="SPDXRef-DOCUMENT",
                                                                 described_spdx_ids=document_dict.get(
                                                                     "documentDescribes"),
                                                                 existing_relationships=[])

    assert len(relationships) == 3
    TestCase().assertCountEqual(relationships,
                                [Relationship("SPDXRef-DOCUMENT", RelationshipType.DESCRIBES, "SPDXRef-Package"),
                                 Relationship("SPDXRef-DOCUMENT", RelationshipType.DESCRIBES, "SPDXRef-File"),
                                 Relationship("SPDXRef-DOCUMENT", RelationshipType.DESCRIBES, "SPDXRef-Snippet")])


def test_parse_document_describes_without_duplicating_relationships():
    relationship_parser = RelationshipParser()
    document_dict = {
        "SPDXID": "SPDXRef-DOCUMENT",
        "documentDescribes": ["SPDXRef-Package", "SPDXRef-File"],
        "relationships": [{"spdxElementId": "SPDXRef-DOCUMENT", "relatedSpdxElement": "SPDXRef-Package",
                           "relationshipType": "DESCRIBES",
                           "comment": "This relationship has a comment."},
                          {"spdxElementId": "SPDXRef-File", "relatedSpdxElement": "SPDXRef-DOCUMENT",
                           "relationshipType": "DESCRIBED_BY", "comment": "This relationship has a comment."}
                          ]}

    relationships = relationship_parser.parse_all_relationships(document_dict)

    assert len(relationships) == 2
    TestCase().assertCountEqual(relationships, [
        Relationship(related_spdx_element_id="SPDXRef-Package", relationship_type=RelationshipType.DESCRIBES,
                     spdx_element_id="SPDXRef-DOCUMENT", comment="This relationship has a comment."),
        Relationship(related_spdx_element_id="SPDXRef-DOCUMENT", relationship_type=RelationshipType.DESCRIBED_BY,
                     spdx_element_id="SPDXRef-File", comment="This relationship has a comment.")])


def test_parse_has_files():
    relationship_parser = RelationshipParser()
    document_dict = {
        "packages":
            [{
                "SPDXID": "SPDXRef-Package",
                "hasFiles": ["SPDXRef-File1", "SPDXRef-File2"]
            }]
    }

    relationships = relationship_parser.parse_has_files(document_dict.get("packages"), existing_relationships=[])

    assert len(relationships) == 2
    TestCase().assertCountEqual(relationships, [
        Relationship(spdx_element_id="SPDXRef-Package", relationship_type=RelationshipType.CONTAINS,
                     related_spdx_element_id="SPDXRef-File1"),
        Relationship(spdx_element_id="SPDXRef-Package", relationship_type=RelationshipType.CONTAINS,
                     related_spdx_element_id="SPDXRef-File2")])


def test_parse_has_files_without_duplicating_relationships():
    relationship_parser = RelationshipParser()
    document_dict = {
        "packages":
            [{
                "SPDXID": "SPDXRef-Package",
                "hasFiles": ["SPDXRef-File1", "SPDXRef-File2"]
            }]
    }
    existing_relationships = [
        Relationship(spdx_element_id="SPDXRef-Package", relationship_type=RelationshipType.CONTAINS,
                     related_spdx_element_id="SPDXRef-File1", comment="This relationship has a comment."),
        Relationship(spdx_element_id="SPDXRef-File2", relationship_type=RelationshipType.CONTAINED_BY,
                     related_spdx_element_id="SPDXRef-Package")]

    relationships = relationship_parser.parse_has_files(document_dict.get("packages"),
                                                        existing_relationships=existing_relationships)

    assert len(relationships) == 0
