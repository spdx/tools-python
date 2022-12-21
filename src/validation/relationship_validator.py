from typing import List

from src.model.document import Document
from src.model.relationship import Relationship, RelationshipType
from src.validation.spdx_id_validators import validate_spdx_id
from src.validation.validation_message import ValidationMessage, ValidationContext, SpdxElementType


def validate_relationships(relationships: List[Relationship], document: Document, spdx_version: str) -> List[ValidationMessage]:
    validation_messages = []
    for relationship in relationships:
        validation_messages.extend(validate_relationship(relationship, document, spdx_version))

    return validation_messages


def validate_relationship(relationship: Relationship, document: Document, spdx_version: str) -> List[ValidationMessage]:
    validation_messages = []
    context = ValidationContext(element_type=SpdxElementType.RELATIONSHIP,
                                full_element=relationship)

    first_id: str = relationship.spdx_element_id
    second_id: str = relationship.related_spdx_element_id
    relationship_type: RelationshipType = relationship.relationship_type

    for spdx_id in [first_id, second_id]:
        messages: List[str] = validate_spdx_id(spdx_id, document, check_document=True)
        for message in messages:
            validation_messages.append(ValidationMessage(message, context))

    if spdx_version != "2.3":
        if relationship_type == RelationshipType.SPECIFICATION_FOR or relationship_type == RelationshipType.REQUIREMENT_DESCRIPTION_FOR:
            validation_messages.append(
                ValidationMessage(f"{relationship_type} is not supported for SPDX versions below 2.3", context))

    return validation_messages
