# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from datetime import datetime

import pytest

from spdx_tools.spdx.datetime_conversions import datetime_from_str, datetime_to_iso_string


def test_datetime_to_iso_string():
    assert datetime_to_iso_string(datetime(2022, 12, 13, 1, 2, 3)) == "2022-12-13T01:02:03Z"


def test_datetime_to_iso_string_with_microseconds():
    assert datetime_to_iso_string(datetime(2022, 12, 13, 1, 2, 3, 666666)) == "2022-12-13T01:02:03Z"


def test_datetime_from_str():
    date_str = "2010-03-04T05:45:11Z"

    date = datetime_from_str(date_str)

    assert date == datetime(2010, 3, 4, 5, 45, 11)


@pytest.mark.parametrize(
    "invalid_date_str, error_type, expected_message",
    [
        (5, TypeError, "Could not convert str to datetime, invalid type: int"),
        ("2010-02-03", ValueError, "time data '2010-02-03' does not match format '%Y-%m-%dT%H:%M:%SZ'"),
    ],
)
def test_datetime_from_str_error(invalid_date_str, error_type, expected_message):
    with pytest.raises(error_type, match=expected_message):
        datetime_from_str(invalid_date_str)
