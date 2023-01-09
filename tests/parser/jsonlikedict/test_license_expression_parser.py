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
from unittest import TestCase

import pytest

from spdx.model.license_expression import LicenseExpression
from spdx.parser.error import SPDXParsingError
from spdx.parser.jsonlikedict.license_expression_parser import LicenseExpressionParser


@pytest.mark.parametrize("invalid_license_expression,expected_message",
                         [(56, ["Error while constructing LicenseExpression: ['SetterError LicenseExpression: "
                                'type of argument "expression_string" must be str; got int instead: 56\']']
                           ), ])
def test_parse_invalid_license_expression(invalid_license_expression, expected_message):
    license_expression_parser = LicenseExpressionParser()

    with pytest.raises(SPDXParsingError) as err:
        license_expression_parser.parse_license_expression(invalid_license_expression)

    TestCase().assertCountEqual(err.value.get_messages(), expected_message)


def test_parse_license_expressions():
    license_expression_parser = LicenseExpressionParser()
    license_expressions_list = ["First License", "Second License", "Third License"]

    license_expressions = license_expression_parser.parse_license_expressions(license_expressions_list)

    assert len(license_expressions) == 3
    TestCase().assertCountEqual(license_expressions,
                                [LicenseExpression("First License"), LicenseExpression("Second License"),
                                 LicenseExpression("Third License")])


@pytest.mark.parametrize("invalid_license_expressions,expected_message", [(["First Expression", 4, 6],
                                                                           [
                                                                               "Error while constructing LicenseExpression: ['SetterError LicenseExpression: "
                                                                               'type of argument "expression_string" must be str; got int instead: 4\']',
                                                                               "Error while constructing LicenseExpression: ['SetterError LicenseExpression: "
                                                                               'type of argument "expression_string" must be str; got int instead: 6\']'])])
def test_parse_invalid_license_expressions(invalid_license_expressions, expected_message):
    license_expression_parser = LicenseExpressionParser()

    with pytest.raises(SPDXParsingError) as err:
        license_expression_parser.parse_license_expressions(invalid_license_expressions)

    TestCase().assertCountEqual(err.value.get_messages(), expected_message)
