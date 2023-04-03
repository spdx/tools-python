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

from spdx3.bump_from_spdx2.bump_utils import handle_no_assertion_or_none
from spdx.model.spdx_no_assertion import SpdxNoAssertion
from spdx.model.spdx_none import SpdxNone


@pytest.mark.parametrize(
    "input_argument,expected_value,expected_stdout",
    [
        (SpdxNone(), None, "test_field: Missing conversion for SpdxNone.\n"),
        (SpdxNoAssertion(), None, ""),
        ("test_string", "test_string", ""),
    ],
)
def test_handle_no_assertion_or_none(input_argument, expected_value, expected_stdout, capsys):
    value = handle_no_assertion_or_none(input_argument, "test_field")

    captured = capsys.readouterr()

    assert value == expected_value
    assert captured.out == expected_stdout
