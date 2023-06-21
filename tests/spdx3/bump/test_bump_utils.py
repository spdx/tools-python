# SPDX-FileCopyrightText: 2022 spdx contributors

# SPDX-License-Identifier: Apache-2.0
import pytest

from spdx_tools.spdx3.bump_from_spdx2.bump_utils import handle_no_assertion_or_none
from spdx_tools.spdx.model.spdx_no_assertion import SpdxNoAssertion
from spdx_tools.spdx.model.spdx_none import SpdxNone


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
