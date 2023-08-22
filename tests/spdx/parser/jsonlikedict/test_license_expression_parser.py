# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from unittest import TestCase

import pytest

from spdx_tools.common.spdx_licensing import spdx_licensing
from spdx_tools.spdx.model import SpdxNoAssertion, SpdxNone
from spdx_tools.spdx.parser.error import SPDXParsingError
from spdx_tools.spdx.parser.jsonlikedict.license_expression_parser import LicenseExpressionParser


@pytest.mark.parametrize(
    "license_expression_str, expected_license",
    [
        ("First License", spdx_licensing.parse("First License")),
        ("Second License", spdx_licensing.parse("Second License")),
        ("NOASSERTION", SpdxNoAssertion()),
        ("NONE", SpdxNone()),
    ],
)
def test_parse_license_expression(license_expression_str, expected_license):
    license_expression_parser = LicenseExpressionParser()
    license_expression = license_expression_parser.parse_license_expression(license_expression_str)

    assert license_expression == expected_license


@pytest.mark.parametrize(
    "invalid_license_expression,expected_message",
    [
        (56, ["Error parsing LicenseExpression: expression must be a string and not: <class 'int'>: 56"]),
    ],
)
def test_parse_invalid_license_expression(invalid_license_expression, expected_message):
    license_expression_parser = LicenseExpressionParser()

    with pytest.raises(SPDXParsingError) as err:
        license_expression_parser.parse_license_expression(invalid_license_expression)

    TestCase().assertCountEqual(err.value.get_messages(), expected_message)
