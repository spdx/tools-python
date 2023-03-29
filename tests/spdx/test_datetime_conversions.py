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
from datetime import datetime

import pytest

from spdx.datetime_conversions import datetime_from_str, datetime_to_iso_string


def test_datetime_to_iso_string():
    assert datetime_to_iso_string(datetime(2022, 12, 13, 1, 2, 3)) == "2022-12-13T01:02:03Z"


def test_datetime_from_str():
    date_str = "2010-03-04T05:45:11Z"

    date = datetime_from_str(date_str)

    assert date == datetime(2010, 3, 4, 5, 45, 11)


@pytest.mark.parametrize("invalid_date_str, error_type, expected_message",
                         [(5, TypeError, "Could not convert str to datetime, invalid type: int"),
                          ("2010-02-03", ValueError, "time data '2010-02-03' does not match format '%Y-%m-%dT%H:%M:%SZ'")])
def test_datetime_from_str_error(invalid_date_str, error_type, expected_message):
    with pytest.raises(error_type, match=expected_message):
        datetime_from_str(invalid_date_str)
