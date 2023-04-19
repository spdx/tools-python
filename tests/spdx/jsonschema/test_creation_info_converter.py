# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from datetime import datetime

import pytest

from spdx_tools.spdx.datetime_conversions import datetime_to_iso_string
from spdx_tools.spdx.jsonschema.creation_info_converter import CreationInfoConverter
from spdx_tools.spdx.jsonschema.creation_info_properties import CreationInfoProperty
from spdx_tools.spdx.model import Actor, ActorType, CreationInfo, Version
from tests.spdx.fixtures import creation_info_fixture


@pytest.fixture
def converter() -> CreationInfoConverter:
    return CreationInfoConverter()


@pytest.mark.parametrize(
    "creation_info_property,expected",
    [
        (CreationInfoProperty.CREATED, "created"),
        (CreationInfoProperty.CREATORS, "creators"),
        (CreationInfoProperty.LICENSE_LIST_VERSION, "licenseListVersion"),
        (CreationInfoProperty.COMMENT, "comment"),
    ],
)
def test_json_property_names(
    converter: CreationInfoConverter, creation_info_property: CreationInfoProperty, expected: str
):
    assert converter.json_property_name(creation_info_property) == expected


def test_successful_conversion(converter: CreationInfoConverter):
    creators = [Actor(ActorType.PERSON, "personName"), Actor(ActorType.TOOL, "toolName")]
    created = datetime(2022, 12, 1)

    converted_dict = converter.convert(
        creation_info_fixture(
            creators=creators, created=created, creator_comment="comment", license_list_version=Version(1, 2)
        )
    )

    assert converted_dict == {
        converter.json_property_name(CreationInfoProperty.CREATED): datetime_to_iso_string(created),
        converter.json_property_name(CreationInfoProperty.CREATORS): ["Person: personName", "Tool: toolName"],
        converter.json_property_name(CreationInfoProperty.LICENSE_LIST_VERSION): "1.2",
        converter.json_property_name(CreationInfoProperty.COMMENT): "comment",
    }


def test_null_values(converter: CreationInfoConverter):
    creation_info = creation_info_fixture(license_list_version=None, creator_comment=None, creators=[])

    converted_dict = converter.convert(creation_info)

    assert converter.json_property_name(CreationInfoProperty.LICENSE_LIST_VERSION) not in converted_dict
    assert converter.json_property_name(CreationInfoProperty.COMMENT) not in converted_dict
    assert converter.json_property_name(CreationInfoProperty.CREATORS) not in converted_dict


def test_json_type(converter: CreationInfoConverter):
    assert converter.get_json_type() == CreationInfoProperty


def test_data_model_type(converter: CreationInfoConverter):
    assert converter.get_data_model_type() == CreationInfo
