from typing import List

from src.model.relationship import Relationship
from src.validation.validation_message import ValidationMessage


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
        pass
