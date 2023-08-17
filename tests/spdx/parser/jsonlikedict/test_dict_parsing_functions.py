# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from unittest import TestCase

import pytest

from spdx_tools.spdx.model import SpdxNoAssertion, SpdxNone
from spdx_tools.spdx.parser.error import SPDXParsingError
from spdx_tools.spdx.parser.jsonlikedict.dict_parsing_functions import (
    json_str_to_enum_name,
    parse_field_or_no_assertion,
    parse_field_or_no_assertion_or_none,
)


def test_json_str_to_enum():
    json_str = "BLAKE2b-256"

    enum_name = json_str_to_enum_name(json_str)

    assert enum_name == "BLAKE2B_256"


@pytest.mark.parametrize("invalid_json_str,expected_message", [(5, ["Type for enum must be str not int"])])
def test_invalid_json_str_to_enum(invalid_json_str, expected_message):
    with pytest.raises(SPDXParsingError) as err:
        json_str_to_enum_name(invalid_json_str)

    TestCase().assertCountEqual(err.value.get_messages(), expected_message)


@pytest.mark.parametrize("input_str,expected_type", [("NOASSERTION", SpdxNoAssertion), ("example string", str)])
def test_parse_field_or_no_assertion(input_str, expected_type):
    resulting_value = parse_field_or_no_assertion(input_str, lambda x: x)

    assert isinstance(resulting_value, expected_type)


@pytest.mark.parametrize(
    "input_str,expected_type", [("NOASSERTION", SpdxNoAssertion), ("NONE", SpdxNone), ("example string", str)]
)
def test_parse_field_or_no_assertion_or_none(input_str, expected_type):
    resulting_value = parse_field_or_no_assertion_or_none(input_str, lambda x: x)

    assert isinstance(resulting_value, expected_type)
