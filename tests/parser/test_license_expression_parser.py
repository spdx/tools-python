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
from src.model.spdx_no_assertion import SpdxNoAssertion
from src.model.spdx_none import SpdxNone
from src.parser.json.license_expression_parser import LicenseExpressionParser


def test_license_expression_parser():
    license_expression_parser = LicenseExpressionParser()
    license_expression_str= "License-Ref1"

    license_expression = license_expression_parser.parse_license_expression(license_expression=license_expression_str)

    assert license_expression.expression_string == "License-Ref1"

def test_license_expression_no_assert():
    license_expression_parser = LicenseExpressionParser()
    license_expression_str= "NOASSERTION"

    spdx_no_assertion = license_expression_parser.parse_license_expression(license_expression=license_expression_str)

    assert type(spdx_no_assertion) == SpdxNoAssertion

def test_license_expression_none():
    license_expression_parser = LicenseExpressionParser()
    license_expression_str = "NONE"

    spdx_none = license_expression_parser.parse_license_expression(
        license_expression=license_expression_str)

    assert type(spdx_none) == SpdxNone


