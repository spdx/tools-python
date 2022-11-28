from typing import List

from src.model.relationship import Relationship, RelationshipType
from src.validation.validation_message import ValidationMessage, ValidationContext, SpdxElementType


class RelationshipValidator:
    spdx_version: str

    def __init__(self, spdx_version):
        self.spdx_version = spdx_version

    def validate_relationships(self, relationships: List[Relationship]) -> List[ValidationMessage]:
        error_messages = []
        for relationship in relationships:
            error_messages.extend(self.validate_relationship(relationship))

        return error_messages

    def validate_relationship(self, relationship: Relationship) -> List[ValidationMessage]:
        validation_messages = []
        context = ValidationContext(element_type=SpdxElementType.RELATIONSHIP, full_element=relationship)

        type_message = "{} must be {}, but is {}: {}"

        if not isinstance(relationship.spdx_element_id, str):
            message = type_message.format("spdx_element_id", str, type(relationship.spdx_element_id), relationship.spdx_element_id)
            validation_messages.append(ValidationMessage(message, context))

        if not isinstance(relationship.relationship_type, RelationshipType):
            message = type_message.format("relationship_type", RelationshipType, type(relationship.relationship_type), relationship.relationship_type)
            validation_messages.append(ValidationMessage(message, context))

        if not isinstance(relationship.related_spdx_element_id, str):
            message = type_message.format("related_spdx_element_id", str, type(relationship.related_spdx_element_id), relationship.related_spdx_element_id)
            validation_messages.append(ValidationMessage(message, context))

        if relationship.comment is not None and not isinstance(relationship.comment, str):
            message = type_message.format("comment", str, type(relationship.comment), relationship.comment)
            validation_messages.append(ValidationMessage(message, context))

        if self.spdx_version != "2.3":
            if relationship.relationship_type == RelationshipType.SPECIFICATION_FOR or relationship.relationship_type == RelationshipType.REQUIREMENT_DESCRIPTION_FOR:
                message = f"{relationship.relationship_type} is not supported for SPDX versions below 2.3"
                validation_messages.append(ValidationMessage(message, context))

        return validation_messages
