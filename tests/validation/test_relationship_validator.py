from typing import List

from src.model.relationship import Relationship, RelationshipType
from src.validation.relationship_validator import RelationshipValidator
from src.validation.validation_message import ValidationMessage, SpdxElementType, ValidationContext


def test_correct_relationship():
    # before
    relationship_validator = RelationshipValidator("2.3")

    relationship = Relationship("first_id", RelationshipType.AMENDS, "second_id", comment="comment")
    validation_messages: List[ValidationMessage] = relationship_validator.validate_relationship(relationship)

    assert validation_messages == []


def test_v2_3_only_types():
    relationship_validator = RelationshipValidator("2.2")

    relationship1 = Relationship("first_id", RelationshipType.SPECIFICATION_FOR, "second_id")
    relationship2 = Relationship("first_id", RelationshipType.REQUIREMENT_DESCRIPTION_FOR, "second_id")

    validation_messages: List[ValidationMessage] = relationship_validator.validate_relationships(
        [relationship1, relationship2])

    expected = {ValidationMessage("RelationshipType.SPECIFICATION_FOR is not supported for SPDX versions below 2.3",
                                  ValidationContext(element_type=SpdxElementType.RELATIONSHIP,
                                                    full_element=relationship1)),
                ValidationMessage(
                    "RelationshipType.REQUIREMENT_DESCRIPTION_FOR is not supported for SPDX versions below 2.3",
                    ValidationContext(element_type=SpdxElementType.RELATIONSHIP, full_element=relationship2))}

    assert set(validation_messages) == expected
