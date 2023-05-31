# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0

from spdx_tools.spdx.model import Relationship, RelationshipType, SpdxNoAssertion


def test_correct_initialization():
    relationship = Relationship("id", RelationshipType.OTHER, SpdxNoAssertion(), "comment")
    assert relationship.spdx_element_id == "id"
    assert relationship.relationship_type == RelationshipType.OTHER
    assert relationship.related_spdx_element_id == SpdxNoAssertion()
    assert relationship.comment == "comment"
