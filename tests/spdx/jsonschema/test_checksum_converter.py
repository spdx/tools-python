# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import pytest

from spdx_tools.spdx.jsonschema.checksum_converter import ChecksumConverter
from spdx_tools.spdx.jsonschema.checksum_properties import ChecksumProperty
from spdx_tools.spdx.model import Checksum, ChecksumAlgorithm


@pytest.fixture
def converter() -> ChecksumConverter:
    return ChecksumConverter()


@pytest.mark.parametrize(
    "checksum_property,expected",
    [(ChecksumProperty.ALGORITHM, "algorithm"), (ChecksumProperty.CHECKSUM_VALUE, "checksumValue")],
)
def test_json_property_names(converter: ChecksumConverter, checksum_property: ChecksumProperty, expected: str):
    assert converter.json_property_name(checksum_property) == expected


def test_successful_conversion(converter: ChecksumConverter):
    checksum = Checksum(ChecksumAlgorithm.SHA1, "123")

    converted_dict = converter.convert(checksum)

    assert converted_dict == {
        converter.json_property_name(ChecksumProperty.ALGORITHM): "SHA1",
        converter.json_property_name(ChecksumProperty.CHECKSUM_VALUE): "123",
    }


def test_json_type(converter: ChecksumConverter):
    assert converter.get_json_type() == ChecksumProperty


def test_data_model_type(converter: ChecksumConverter):
    assert converter.get_data_model_type() == Checksum
