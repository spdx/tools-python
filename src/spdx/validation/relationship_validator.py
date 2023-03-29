# Copyright (c) 2022 spdx contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import List

from spdx.model.document import Document
from spdx.model.relationship import Relationship, RelationshipType
from spdx.model.spdx_no_assertion import SpdxNoAssertion
from spdx.model.spdx_none import SpdxNone
from spdx.validation.spdx_id_validators import validate_spdx_id
from spdx.validation.validation_message import ValidationMessage, ValidationContext, SpdxElementType


def validate_relationships(relationships: List[Relationship], spdx_version: str, document: Document) -> List[
    ValidationMessage]:
    validation_messages = []
    for relationship in relationships:
        validation_messages.extend(validate_relationship(relationship, spdx_version, document))

    return validation_messages


def validate_relationship(relationship: Relationship, spdx_version: str, document: Document) -> List[ValidationMessage]:
    validation_messages = []
    context = ValidationContext(element_type=SpdxElementType.RELATIONSHIP,
                                full_element=relationship)

    relationship_type: RelationshipType = relationship.relationship_type

    messages: List[str] = validate_spdx_id(relationship.spdx_element_id, document, check_document=True)
    for message in messages:
        validation_messages.append(ValidationMessage(message, context))

    if relationship.related_spdx_element_id not in [SpdxNone(), SpdxNoAssertion()]:
        messages: List[str] = validate_spdx_id(relationship.related_spdx_element_id, document, check_document=True)
        for message in messages:
            validation_messages.append(ValidationMessage(message, context))

    if spdx_version == "SPDX-2.2":
        if relationship_type == RelationshipType.SPECIFICATION_FOR or relationship_type == RelationshipType.REQUIREMENT_DESCRIPTION_FOR:
            validation_messages.append(
                ValidationMessage(f"{relationship_type} is not supported in SPDX-2.2", context))

    return validation_messages
