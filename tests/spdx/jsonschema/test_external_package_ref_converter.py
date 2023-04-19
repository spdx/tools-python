# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import pytest

from spdx_tools.spdx.jsonschema.external_package_ref_converter import ExternalPackageRefConverter
from spdx_tools.spdx.jsonschema.external_package_ref_properties import ExternalPackageRefProperty
from spdx_tools.spdx.model import ExternalPackageRef, ExternalPackageRefCategory


@pytest.fixture
def converter() -> ExternalPackageRefConverter:
    return ExternalPackageRefConverter()


@pytest.mark.parametrize(
    "external_package_ref_property,expected",
    [
        (ExternalPackageRefProperty.COMMENT, "comment"),
        (ExternalPackageRefProperty.REFERENCE_CATEGORY, "referenceCategory"),
        (ExternalPackageRefProperty.REFERENCE_LOCATOR, "referenceLocator"),
        (ExternalPackageRefProperty.REFERENCE_TYPE, "referenceType"),
    ],
)
def test_json_property_names(
    converter: ExternalPackageRefConverter, external_package_ref_property: ExternalPackageRefProperty, expected: str
):
    assert converter.json_property_name(external_package_ref_property) == expected


def test_json_type(converter: ExternalPackageRefConverter):
    assert converter.get_json_type() == ExternalPackageRefProperty


def test_data_model_type(converter: ExternalPackageRefConverter):
    assert converter.get_data_model_type() == ExternalPackageRef


def test_successful_conversion(converter: ExternalPackageRefConverter):
    external_package_ref = ExternalPackageRef(ExternalPackageRefCategory.PACKAGE_MANAGER, "type", "locator", "comment")

    converted_dict = converter.convert(external_package_ref)

    assert converted_dict == {
        converter.json_property_name(ExternalPackageRefProperty.COMMENT): "comment",
        converter.json_property_name(ExternalPackageRefProperty.REFERENCE_CATEGORY): "PACKAGE_MANAGER",
        converter.json_property_name(ExternalPackageRefProperty.REFERENCE_LOCATOR): "locator",
        converter.json_property_name(ExternalPackageRefProperty.REFERENCE_TYPE): "type",
    }
