# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0

import pytest

from spdx_tools.spdx.model import Version


@pytest.mark.parametrize("input_string,expected", [("1.2", Version(1, 2)), ("12.345", Version(12, 345))])
def test_version_from_string(input_string, expected):
    assert Version.is_valid_version_string(input_string)
    version: Version = Version.from_string(input_string)
    assert version == expected


@pytest.mark.parametrize("input_string", ["1", "1-2", "1.a", "a", "a.b", "a.1", "v1.2", "1.2v"])
def test_invalid_version_string(input_string):
    assert not Version.is_valid_version_string(input_string)
    with pytest.raises(ValueError) as error:
        Version.from_string(input_string)
    assert str(error.value) == f"{input_string} is not a valid version string"
