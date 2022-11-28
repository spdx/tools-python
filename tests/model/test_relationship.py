import pytest

from src.model.relationship import Relationship, RelationshipType


def test_correct_initialization():
    relationship = Relationship("id", RelationshipType.OTHER, "other_id", "comment")
    assert relationship.spdx_element_id == "id"
    assert relationship.relationship_type == RelationshipType.OTHER
    assert relationship.related_spdx_element_id == "other_id"
    assert relationship.comment == "comment"


def test_wrong_type_in_spdx_element_id():
    with pytest.raises(TypeError):
        Relationship(42, RelationshipType.OTHER, "other_id", "comment")


def test_wrong_type_in_relationship_type():
    with pytest.raises(TypeError):
        Relationship("id", 42, "other_id", "comment")


def test_wrong_type_in_related_spdx_element_id():
    with pytest.raises(TypeError):
        Relationship("id", RelationshipType.OTHER, 42, "comment")


def test_wrong_type_in_comment():
    with pytest.raises(TypeError):
        Relationship("id", RelationshipType.OTHER, "other_id", 42)
