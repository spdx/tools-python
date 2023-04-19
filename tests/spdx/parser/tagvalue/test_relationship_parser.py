# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import pytest

from spdx_tools.spdx.constants import DOCUMENT_SPDX_ID
from spdx_tools.spdx.model import Relationship, RelationshipType, SpdxNoAssertion, SpdxNone
from spdx_tools.spdx.parser.error import SPDXParsingError
from spdx_tools.spdx.parser.tagvalue.parser import Parser
from tests.spdx.parser.tagvalue.test_creation_info_parser import DOCUMENT_STR


@pytest.mark.parametrize(
    "relationship_str, expected_relationship",
    [
        (
            "\n".join(
                [f"Relationship: {DOCUMENT_SPDX_ID} DESCRIBES SPDXRef-File", "RelationshipComment: This is a comment."]
            ),
            Relationship(DOCUMENT_SPDX_ID, RelationshipType.DESCRIBES, "SPDXRef-File", "This is a comment."),
        ),
        (
            f"Relationship: {DOCUMENT_SPDX_ID} PATCH_FOR NOASSERTION",
            Relationship(DOCUMENT_SPDX_ID, RelationshipType.PATCH_FOR, SpdxNoAssertion()),
        ),
        (
            "Relationship: SPDXRef-CarolCompression DEPENDS_ON NONE",
            Relationship("SPDXRef-CarolCompression", RelationshipType.DEPENDS_ON, SpdxNone()),
        ),
        (
            "Relationship: DocumentRef-ExternalDocument:SPDXRef-Test DEPENDS_ON DocumentRef:AnotherRef",
            Relationship(
                "DocumentRef-ExternalDocument:SPDXRef-Test", RelationshipType.DEPENDS_ON, "DocumentRef:AnotherRef"
            ),
        ),
    ],
)
def test_parse_relationship(relationship_str, expected_relationship):
    parser = Parser()
    document = parser.parse("\n".join([DOCUMENT_STR, relationship_str]))
    assert document is not None
    assert len(document.relationships) == 1
    relationship = document.relationships[0]
    assert relationship == expected_relationship


@pytest.mark.parametrize(
    "relationship_str, expected_message",
    [
        (
            "Relationship: spdx_id DESCRIBES",
            [
                "Error while parsing Relationship: [\"Relationship couldn't be split in "
                'spdx_element_id, relationship_type and related_spdx_element. Line: 1"]'
            ],
        ),
        (
            "Relationship: spdx_id IS spdx_id",
            ["Error while parsing Relationship: ['Invalid RelationshipType IS. Line: 1']"],
        ),
    ],
)
def test_parse_invalid_relationship(relationship_str, expected_message):
    parser = Parser()
    with pytest.raises(SPDXParsingError) as err:
        parser.parse(relationship_str)

    assert err.value.get_messages() == expected_message
