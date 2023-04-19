# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import pytest

from spdx_tools.spdx.jsonschema.relationship_converter import RelationshipConverter
from spdx_tools.spdx.jsonschema.relationship_properties import RelationshipProperty
from spdx_tools.spdx.model import Relationship, RelationshipType, SpdxNoAssertion, SpdxNone
from spdx_tools.spdx.model.spdx_no_assertion import SPDX_NO_ASSERTION_STRING
from spdx_tools.spdx.model.spdx_none import SPDX_NONE_STRING
from tests.spdx.fixtures import relationship_fixture


@pytest.fixture
def converter() -> RelationshipConverter:
    return RelationshipConverter()


@pytest.mark.parametrize(
    "relationship_property,expected",
    [
        (RelationshipProperty.SPDX_ELEMENT_ID, "spdxElementId"),
        (RelationshipProperty.COMMENT, "comment"),
        (RelationshipProperty.RELATED_SPDX_ELEMENT, "relatedSpdxElement"),
        (RelationshipProperty.RELATIONSHIP_TYPE, "relationshipType"),
    ],
)
def test_json_property_names(
    converter: RelationshipConverter, relationship_property: RelationshipProperty, expected: str
):
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
        converter.json_property_name(RelationshipProperty.RELATIONSHIP_TYPE): "COPY_OF",
    }


def test_spdx_no_assertion(converter: RelationshipConverter):
    relationship = relationship_fixture(related_spdx_element_id=SpdxNoAssertion())

    converted_dict = converter.convert(relationship)

    assert (
        converted_dict[converter.json_property_name(RelationshipProperty.RELATED_SPDX_ELEMENT)]
        == SPDX_NO_ASSERTION_STRING
    )


def test_spdx_none(converter: RelationshipConverter):
    relationship = relationship_fixture(related_spdx_element_id=SpdxNone())

    converted_dict = converter.convert(relationship)

    assert converted_dict[converter.json_property_name(RelationshipProperty.RELATED_SPDX_ELEMENT)] == SPDX_NONE_STRING
