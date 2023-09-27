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
        (56, ["Error parsing LicenseExpression: \"56\": expression must be a string and not: <class 'int'>"]),
        (
            "LGPL-2.1, GPL-2.0, GPL-3.0",
            [
                "Error parsing LicenseExpression: \"LGPL-2.1, GPL-2.0, GPL-3.0\": Invalid license key: the valid characters are: letters and numbers, underscore, dot, colon or hyphen signs and spaces: 'LGPL-2.1, GPL-2.0, GPL-3.0'"  # noqa: E501
            ],
        ),
        ("Apache License (2.0)", ['Error parsing LicenseExpression: "Apache License (2.0)"']),
    ],
)
def test_parse_invalid_license_expression(invalid_license_expression, expected_message):
    license_expression_parser = LicenseExpressionParser()

    with pytest.raises(SPDXParsingError) as err:
        license_expression_parser.parse_license_expression(invalid_license_expression)

    TestCase().assertCountEqual(err.value.get_messages(), expected_message)
