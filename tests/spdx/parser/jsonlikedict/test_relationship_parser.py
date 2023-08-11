# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from unittest import TestCase

import pytest

from spdx_tools.spdx.constants import DOCUMENT_SPDX_ID
from spdx_tools.spdx.model import Relationship, RelationshipType, SpdxNoAssertion
from spdx_tools.spdx.parser.error import SPDXParsingError
from spdx_tools.spdx.parser.jsonlikedict.relationship_parser import RelationshipParser


def test_parse_relationship():
    relationship_parser = RelationshipParser()

    relationship_dict = {
        "spdxElementId": DOCUMENT_SPDX_ID,
        "relationshipType": "CONTAINS",
        "relatedSpdxElement": "NOASSERTION",
        "comment": "Comment.",
    }

    relationship = relationship_parser.parse_relationship(relationship_dict)

    assert relationship.relationship_type == RelationshipType.CONTAINS
    assert relationship.spdx_element_id == DOCUMENT_SPDX_ID
    assert relationship.related_spdx_element_id == SpdxNoAssertion()
    assert relationship.comment == "Comment."


def test_parse_incomplete_relationship():
    relationship_parser = RelationshipParser()
    relationship_dict = {
        "spdxElementId": DOCUMENT_SPDX_ID,
        "relatedSpdxElement": "SPDXRef-Package",
        "comment": "Comment.",
    }

    with pytest.raises(SPDXParsingError):
        relationship_parser.parse_relationship(relationship_dict)


def test_parse_relationship_type():
    relationship_parser = RelationshipParser()
    relationship_type_str = "DEPENDENCY_OF"

    relationship_type = relationship_parser.parse_relationship_type(relationship_type_str)
    assert relationship_type == RelationshipType.DEPENDENCY_OF


def test_parse_document_describes():
    relationship_parser = RelationshipParser()

    document_dict = {
        "SPDXID": DOCUMENT_SPDX_ID,
        "documentDescribes": ["SPDXRef-Package", "SPDXRef-File", "SPDXRef-Snippet"],
    }

    relationships = relationship_parser.parse_document_describes(
        doc_spdx_id=DOCUMENT_SPDX_ID,
        described_spdx_ids=document_dict.get("documentDescribes"),
        existing_relationships=[],
    )

    assert len(relationships) == 3
    TestCase().assertCountEqual(
        relationships,
        [
            Relationship(DOCUMENT_SPDX_ID, RelationshipType.DESCRIBES, "SPDXRef-Package"),
            Relationship(DOCUMENT_SPDX_ID, RelationshipType.DESCRIBES, "SPDXRef-File"),
            Relationship(DOCUMENT_SPDX_ID, RelationshipType.DESCRIBES, "SPDXRef-Snippet"),
        ],
    )


@pytest.mark.parametrize(
    "document_describes,relationships,parsed_relationships",
    [
        (
            ["SPDXRef-Package", "SPDXRef-File"],
            [
                {
                    "spdxElementId": DOCUMENT_SPDX_ID,
                    "relatedSpdxElement": "SPDXRef-Package",
                    "relationshipType": "DESCRIBES",
                    "comment": "This relationship has a comment.",
                },
                {
                    "spdxElementId": "SPDXRef-File",
                    "relatedSpdxElement": DOCUMENT_SPDX_ID,
                    "relationshipType": "DESCRIBED_BY",
                    "comment": "This relationship has a comment.",
                },
            ],
            [
                Relationship(
                    related_spdx_element_id="SPDXRef-Package",
                    relationship_type=RelationshipType.DESCRIBES,
                    spdx_element_id=DOCUMENT_SPDX_ID,
                    comment="This relationship has a comment.",
                ),
                Relationship(
                    related_spdx_element_id=DOCUMENT_SPDX_ID,
                    relationship_type=RelationshipType.DESCRIBED_BY,
                    spdx_element_id="SPDXRef-File",
                    comment="This relationship has a comment.",
                ),
            ],
        ),
        (
            ["SPDXRef-Package", "SPDXRef-File", "SPDXRef-Package"],
            [],
            [
                Relationship(
                    related_spdx_element_id="SPDXRef-Package",
                    relationship_type=RelationshipType.DESCRIBES,
                    spdx_element_id=DOCUMENT_SPDX_ID,
                ),
                Relationship(
                    related_spdx_element_id="SPDXRef-File",
                    relationship_type=RelationshipType.DESCRIBES,
                    spdx_element_id=DOCUMENT_SPDX_ID,
                ),
            ],
        ),
    ],
)
def test_parse_document_describes_without_duplicating_relationships(
    document_describes, relationships, parsed_relationships
):
    relationship_parser = RelationshipParser()
    document_dict = {
        "SPDXID": DOCUMENT_SPDX_ID,
        "documentDescribes": document_describes,
        "relationships": relationships,
    }

    relationships = relationship_parser.parse_all_relationships(document_dict)

    assert len(relationships) == len(parsed_relationships)
    TestCase().assertCountEqual(relationships, parsed_relationships)


def test_parse_has_files():
    relationship_parser = RelationshipParser()
    document_dict = {"packages": [{"SPDXID": "SPDXRef-Package", "hasFiles": ["SPDXRef-File1", "SPDXRef-File2"]}]}

    relationships = relationship_parser.parse_has_files(document_dict.get("packages"), existing_relationships=[])

    assert len(relationships) == 2
    TestCase().assertCountEqual(
        relationships,
        [
            Relationship(
                spdx_element_id="SPDXRef-Package",
                relationship_type=RelationshipType.CONTAINS,
                related_spdx_element_id="SPDXRef-File1",
            ),
            Relationship(
                spdx_element_id="SPDXRef-Package",
                relationship_type=RelationshipType.CONTAINS,
                related_spdx_element_id="SPDXRef-File2",
            ),
        ],
    )


@pytest.mark.parametrize(
    "has_files,existing_relationships,contains_relationships",
    [
        # pre-requisite for parse_has_files requires that comments in relationships are stripped
        (
            ["SPDXRef-File1", "SPDXRef-File2"],
            [
                Relationship(
                    spdx_element_id="SPDXRef-Package",
                    relationship_type=RelationshipType.CONTAINS,
                    related_spdx_element_id="SPDXRef-File1",
                ),
                Relationship(
                    spdx_element_id="SPDXRef-File2",
                    relationship_type=RelationshipType.CONTAINED_BY,
                    related_spdx_element_id="SPDXRef-Package",
                ),
            ],
            [],
        ),
        (
            ["SPDXRef-File1", "SPDXRef-File2", "SPDXRef-File1"],
            [],
            [
                Relationship(
                    spdx_element_id="SPDXRef-Package",
                    relationship_type=RelationshipType.CONTAINS,
                    related_spdx_element_id="SPDXRef-File1",
                ),
                Relationship(
                    spdx_element_id="SPDXRef-Package",
                    relationship_type=RelationshipType.CONTAINS,
                    related_spdx_element_id="SPDXRef-File2",
                ),
            ],
        ),
    ],
)
def test_parse_has_files_without_duplicating_relationships(has_files, existing_relationships, contains_relationships):
    relationship_parser = RelationshipParser()
    document_dict = {"packages": [{"SPDXID": "SPDXRef-Package", "hasFiles": has_files}]}
    relationships = relationship_parser.parse_has_files(
        document_dict.get("packages"), existing_relationships=existing_relationships
    )

    assert len(relationships) == len(contains_relationships)
    TestCase().assertCountEqual(relationships, contains_relationships)
