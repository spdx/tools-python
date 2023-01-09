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

from spdx.jsonschema.checksum_converter import ChecksumConverter
from spdx.jsonschema.checksum_properties import ChecksumProperty
from spdx.model.checksum import Checksum, ChecksumAlgorithm


@pytest.fixture
def converter() -> ChecksumConverter:
    return ChecksumConverter()


@pytest.mark.parametrize("checksum_property,expected", [(ChecksumProperty.ALGORITHM, "algorithm"),
                                                        (ChecksumProperty.CHECKSUM_VALUE, "checksumValue")])
def test_json_property_names(converter: ChecksumConverter, checksum_property: ChecksumProperty, expected: str):
    assert converter.json_property_name(checksum_property) == expected


def test_successful_conversion(converter: ChecksumConverter):
    checksum = Checksum(ChecksumAlgorithm.SHA1, "123")

    converted_dict = converter.convert(checksum)

    assert converted_dict == {
        converter.json_property_name(ChecksumProperty.ALGORITHM): "SHA1",
        converter.json_property_name(ChecksumProperty.CHECKSUM_VALUE): "123"
    }


def test_json_type(converter: ChecksumConverter):
    assert converter.get_json_type() == ChecksumProperty


def test_data_model_type(converter: ChecksumConverter):
    assert converter.get_data_model_type() == Checksum
