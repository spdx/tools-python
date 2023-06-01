# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0

import pytest

from spdx_tools.spdx.model import Relationship, RelationshipType, SpdxNoAssertion


def test_correct_initialization():
    relationship = Relationship("id", RelationshipType.OTHER, SpdxNoAssertion(), "comment")
    assert relationship.spdx_element_id == "id"
    assert relationship.relationship_type == RelationshipType.OTHER
    assert relationship.related_spdx_element_id == SpdxNoAssertion()
    assert relationship.comment == "comment"


def test_wrong_type_in_spdx_element_id():
    with pytest.raises(TypeError):
        Relationship(SpdxNoAssertion(), RelationshipType.OTHER, "other_id")


def test_wrong_type_in_relationship_type():
    with pytest.raises(TypeError):
        Relationship("id", 42, "other_id")


def test_wrong_type_in_related_spdx_element_id():
    with pytest.raises(TypeError):
        Relationship("id", RelationshipType.OTHER, 42)


def test_wrong_type_in_comment():
    with pytest.raises(TypeError):
        Relationship("id", RelationshipType.OTHER, "other_id", 42)
