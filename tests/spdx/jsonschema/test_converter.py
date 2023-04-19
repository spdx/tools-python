# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from enum import auto
from typing import Any, Type

import pytest

from spdx_tools.common.typing.dataclass_with_properties import dataclass_with_properties
from spdx_tools.common.typing.type_checks import check_types_and_set_values
from spdx_tools.spdx.jsonschema.converter import TypedConverter
from spdx_tools.spdx.jsonschema.json_property import JsonProperty
from spdx_tools.spdx.model import Checksum, ChecksumAlgorithm, Document


class TestPropertyType(JsonProperty):
    FIRST_NAME = auto()
    SECOND_NAME = auto()


@dataclass_with_properties
class TestDataModelType:
    first_property: str
    second_property: int
    third_property: int

    def __init__(self, first_property: str, second_property: int, third_property: int):
        check_types_and_set_values(self, locals())


class TestConverter(TypedConverter):
    def json_property_name(self, test_property: TestPropertyType) -> str:
        if test_property == TestPropertyType.FIRST_NAME:
            return "jsonFirstName"
        else:
            return "jsonSecondName"

    def _get_property_value(
        self, instance: TestDataModelType, test_property: TestPropertyType, _document: Document = None
    ) -> Any:
        if test_property == TestPropertyType.FIRST_NAME:
            return instance.first_property
        elif test_property == TestPropertyType.SECOND_NAME:
            return instance.second_property + instance.third_property

    def get_json_type(self) -> Type[JsonProperty]:
        return TestPropertyType

    def get_data_model_type(self) -> Type:
        return TestDataModelType


def test_conversion():
    converter = TestConverter()
    test_instance = TestDataModelType("firstPropertyValue", 1, 2)

    converted_dict = converter.convert(test_instance)

    assert converted_dict == {"jsonFirstName": "firstPropertyValue", "jsonSecondName": 3}


def test_wrong_type():
    converter = TestConverter()
    checksum = Checksum(ChecksumAlgorithm.SHA1, "123")

    with pytest.raises(TypeError) as error:
        converter.convert(checksum)

    error_message: str = error.value.args[0]
    assert TestConverter.__name__ in error_message
    assert TestDataModelType.__name__ in error_message
    assert Checksum.__name__ in error_message
