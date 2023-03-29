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

from spdx.jsonschema.package_verification_code_converter import PackageVerificationCodeConverter
from spdx.jsonschema.package_verification_code_properties import PackageVerificationCodeProperty
from spdx.model.package import PackageVerificationCode


@pytest.fixture
def converter() -> PackageVerificationCodeConverter:
    return PackageVerificationCodeConverter()


@pytest.mark.parametrize("package_verification_code_property,expected",
                         [(PackageVerificationCodeProperty.PACKAGE_VERIFICATION_CODE_EXCLUDED_FILES,
                           "packageVerificationCodeExcludedFiles"),
                          (PackageVerificationCodeProperty.PACKAGE_VERIFICATION_CODE_VALUE,
                           "packageVerificationCodeValue")])
def test_json_property_names(converter: PackageVerificationCodeConverter,
                             package_verification_code_property: PackageVerificationCodeProperty, expected: str):
    assert converter.json_property_name(package_verification_code_property) == expected


def test_json_type(converter: PackageVerificationCodeConverter):
    assert converter.get_json_type() == PackageVerificationCodeProperty


def test_data_model_type(converter: PackageVerificationCodeConverter):
    assert converter.get_data_model_type() == PackageVerificationCode


def test_successful_conversion(converter: PackageVerificationCodeConverter):
    package_verification_code = PackageVerificationCode("value", ["file1", "file2"])

    converted_dict = converter.convert(package_verification_code)

    assert converted_dict == {
        converter.json_property_name(PackageVerificationCodeProperty.PACKAGE_VERIFICATION_CODE_EXCLUDED_FILES): [
            "file1", "file2"],
        converter.json_property_name(PackageVerificationCodeProperty.PACKAGE_VERIFICATION_CODE_VALUE): "value"
    }


def test_null_values(converter: PackageVerificationCodeConverter):
    package_verification_code = PackageVerificationCode("value")

    converted_dict = converter.convert(package_verification_code)

    assert converter.json_property_name(
        PackageVerificationCodeProperty.PACKAGE_VERIFICATION_CODE_EXCLUDED_FILES) not in converted_dict
