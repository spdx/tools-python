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
import pytest

from spdx.jsonschema.relationship_converter import RelationshipConverter
from spdx.jsonschema.relationship_properties import RelationshipProperty
from spdx.model.relationship import Relationship, RelationshipType
from spdx.model.spdx_no_assertion import SpdxNoAssertion, SPDX_NO_ASSERTION_STRING
from spdx.model.spdx_none import SpdxNone, SPDX_NONE_STRING
from tests.spdx.fixtures import relationship_fixture


@pytest.fixture
def converter() -> RelationshipConverter:
    return RelationshipConverter()


@pytest.mark.parametrize("relationship_property,expected",
                         [(RelationshipProperty.SPDX_ELEMENT_ID, "spdxElementId"),
                          (RelationshipProperty.COMMENT, "comment"),
                          (RelationshipProperty.RELATED_SPDX_ELEMENT, "relatedSpdxElement"),
                          (RelationshipProperty.RELATIONSHIP_TYPE, "relationshipType")])
def test_json_property_names(converter: RelationshipConverter, relationship_property: RelationshipProperty,
                             expected: str):
    assert converter.json_property_name(relationship_property) == expected


def test_json_type(converter: RelationshipConverter):
    assert converter.get_json_type() == RelationshipProperty


def test_data_model_type(converter: RelationshipConverter):
    assert converter.get_data_model_type() == Relationship


def test_successful_conversion(converter: RelationshipConverter):
    relationship = Relationship("spdxElementId", RelationshipType.COPY_OF, "relatedElementId", "comment")

    converted_dict = converter.convert(relationship)

    assert converted_dict == {
        converter.json_property_name(RelationshipProperty.SPDX_ELEMENT_ID): "spdxElementId",
        converter.json_property_name(RelationshipProperty.COMMENT): "comment",
        converter.json_property_name(RelationshipProperty.RELATED_SPDX_ELEMENT): "relatedElementId",
        converter.json_property_name(RelationshipProperty.RELATIONSHIP_TYPE): "COPY_OF"
    }


def test_spdx_no_assertion(converter: RelationshipConverter):
    relationship = relationship_fixture(related_spdx_element_id=SpdxNoAssertion())

    converted_dict = converter.convert(relationship)

    assert converted_dict[
               converter.json_property_name(RelationshipProperty.RELATED_SPDX_ELEMENT)] == SPDX_NO_ASSERTION_STRING


def test_spdx_none(converter: RelationshipConverter):
    relationship = relationship_fixture(related_spdx_element_id=SpdxNone())

    converted_dict = converter.convert(relationship)

    assert converted_dict[converter.json_property_name(RelationshipProperty.RELATED_SPDX_ELEMENT)] == SPDX_NONE_STRING
