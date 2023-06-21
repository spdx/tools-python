# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0

from beartype.typing import List

from spdx_tools.spdx.model import Document, Relationship, RelationshipType, SpdxNoAssertion, SpdxNone
from spdx_tools.spdx.validation.spdx_id_validators import validate_spdx_id
from spdx_tools.spdx.validation.validation_message import SpdxElementType, ValidationContext, ValidationMessage


def validate_relationships(
    relationships: List[Relationship], spdx_version: str, document: Document
) -> List[ValidationMessage]:
    validation_messages = []
    for relationship in relationships:
        validation_messages.extend(validate_relationship(relationship, spdx_version, document))

    return validation_messages


def validate_relationship(
    relationship: Relationship, spdx_version: str, document: Document
) -> List[ValidationMessage]:
    validation_messages = []
    context = ValidationContext(element_type=SpdxElementType.RELATIONSHIP, full_element=relationship)

    relationship_type: RelationshipType = relationship.relationship_type

    messages: List[str] = validate_spdx_id(relationship.spdx_element_id, document, check_document=True)
    for message in messages:
        validation_messages.append(ValidationMessage(message, context))

    if relationship.related_spdx_element_id not in [SpdxNone(), SpdxNoAssertion()]:
        messages: List[str] = validate_spdx_id(relationship.related_spdx_element_id, document, check_document=True)
        for message in messages:
            validation_messages.append(ValidationMessage(message, context))

    if spdx_version == "SPDX-2.2":
        if (
            relationship_type == RelationshipType.SPECIFICATION_FOR
            or relationship_type == RelationshipType.REQUIREMENT_DESCRIPTION_FOR
        ):
            validation_messages.append(ValidationMessage(f"{relationship_type} is not supported in SPDX-2.2", context))

    return validation_messages
