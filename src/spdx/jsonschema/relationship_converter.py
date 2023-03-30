# SPDX-FileCopyrightText: 2022 spdx contributors

# SPDX-License-Identifier: Apache-2.0
from typing import Any, Type

from spdx.jsonschema.converter import TypedConverter
from spdx.jsonschema.json_property import JsonProperty
from spdx.jsonschema.relationship_properties import RelationshipProperty
from spdx.model.document import Document
from spdx.model.relationship import Relationship


class RelationshipConverter(TypedConverter[Relationship]):
    def _get_property_value(
        self, relationship: Relationship, relationship_property: RelationshipProperty, document: Document = None
    ) -> Any:
        if relationship_property == RelationshipProperty.SPDX_ELEMENT_ID:
            return relationship.spdx_element_id
        elif relationship_property == RelationshipProperty.COMMENT:
            return relationship.comment
        elif relationship_property == RelationshipProperty.RELATED_SPDX_ELEMENT:
            return str(relationship.related_spdx_element_id)
        elif relationship_property == RelationshipProperty.RELATIONSHIP_TYPE:
            return relationship.relationship_type.name

    def get_json_type(self) -> Type[JsonProperty]:
        return RelationshipProperty

    def get_data_model_type(self) -> Type[Relationship]:
        return Relationship
