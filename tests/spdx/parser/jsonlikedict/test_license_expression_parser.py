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
from license_expression import get_spdx_licensing

from spdx.model.spdx_no_assertion import SpdxNoAssertion
from spdx.model.spdx_none import SpdxNone
from spdx.parser.error import SPDXParsingError
from spdx.parser.jsonlikedict.license_expression_parser import LicenseExpressionParser


@pytest.mark.parametrize("license_expression_str, expected_license",
                         [("First License", get_spdx_licensing().parse("First License")),
                          ("Second License", get_spdx_licensing().parse("Second License")),
                          ("NOASSERTION", SpdxNoAssertion()),
                          ("NONE", SpdxNone())])
def test_parse_license_expression(license_expression_str, expected_license):
    license_expression_parser = LicenseExpressionParser()
    license_expression = license_expression_parser.parse_license_expression(license_expression_str)

    assert license_expression == expected_license


@pytest.mark.parametrize("invalid_license_expression,expected_message",
                         [(56,
                           ["Error parsing LicenseExpression: expression must be a string and not: <class 'int'>: 56"]),
                          ])
def test_parse_invalid_license_expression(invalid_license_expression, expected_message):
    license_expression_parser = LicenseExpressionParser()

    with pytest.raises(SPDXParsingError) as err:
        license_expression_parser.parse_license_expression(invalid_license_expression)

    TestCase().assertCountEqual(err.value.get_messages(), expected_message)
