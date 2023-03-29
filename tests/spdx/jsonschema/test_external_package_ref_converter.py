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

from spdx.jsonschema.external_package_ref_converter import ExternalPackageRefConverter
from spdx.jsonschema.external_package_ref_properties import ExternalPackageRefProperty
from spdx.model.package import ExternalPackageRef, ExternalPackageRefCategory


@pytest.fixture
def converter() -> ExternalPackageRefConverter:
    return ExternalPackageRefConverter()


@pytest.mark.parametrize("external_package_ref_property,expected",
                         [(ExternalPackageRefProperty.COMMENT, "comment"),
                          (ExternalPackageRefProperty.REFERENCE_CATEGORY, "referenceCategory"),
                          (ExternalPackageRefProperty.REFERENCE_LOCATOR, "referenceLocator"),
                          (ExternalPackageRefProperty.REFERENCE_TYPE, "referenceType")])
def test_json_property_names(converter: ExternalPackageRefConverter,
                             external_package_ref_property: ExternalPackageRefProperty, expected: str):
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
        converter.json_property_name(ExternalPackageRefProperty.REFERENCE_TYPE): "type"
    }
