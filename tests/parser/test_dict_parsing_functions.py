#  Copyright (c) 2022 spdx contributors
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#    http://www.apache.org/licenses/LICENSE-2.0
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
from datetime import datetime
from unittest import TestCase

import pytest

from src.model.spdx_no_assertion import SpdxNoAssertion
from src.model.spdx_none import SpdxNone
from src.parser.error import SPDXParsingError
from src.parser.json.dict_parsing_functions import datetime_from_str, json_str_to_enum_name, \
    parse_field_or_no_assertion, parse_field_or_no_assertion_or_none


def test_datetime_from_str():
    date_str = "2010-03-04T05:45:11Z"

    date = datetime_from_str(date_str)

    assert date == datetime(2010, 3, 4, 5, 45, 11)


@pytest.mark.parametrize("invalid_date_str,expected_message",
                         [(5, ["Could not convert str to datetime, invalid type: int"]),
                          ("2010-02-03", ['Could not convert str to datetime, format of 2010-02-03 does not match '
                                          '"%Y-%m-%dT%H:%M:%SZ"'])])
def test_datetime_from_str_error(invalid_date_str, expected_message):
    with pytest.raises(SPDXParsingError) as err:
        datetime_from_str(invalid_date_str)

    TestCase().assertCountEqual(err.value.get_messages(), expected_message)


def test_json_str_to_enum():
    json_str = "BLAKE2b-256"

    enum_name = json_str_to_enum_name(json_str)

    assert enum_name == "BLAKE2B_256"


@pytest.mark.parametrize("invalid_json_str,expected_message",
                         [(5, ["Type for enum must be str not int"])])
def test_invalid_json_str_to_enum(invalid_json_str, expected_message):
    with pytest.raises(SPDXParsingError) as err:
        json_str_to_enum_name(invalid_json_str)

    TestCase().assertCountEqual(err.value.get_messages(), expected_message)


@pytest.mark.parametrize("input_str,expected_type", [("NOASSERTION", SpdxNoAssertion), ("example string", str)])
def test_parse_field_or_no_assertion(input_str, expected_type):
    resulting_value = parse_field_or_no_assertion(input_str, lambda x: x)

    assert type(resulting_value) == expected_type


@pytest.mark.parametrize("input_str,expected_type",
                         [("NOASSERTION", SpdxNoAssertion), ("NONE", SpdxNone), ("example string", str)])
def test_parse_field_or_no_assertion_or_none(input_str, expected_type):
    resulting_value = parse_field_or_no_assertion_or_none(input_str, lambda x: x)

    assert type(resulting_value) == expected_type
