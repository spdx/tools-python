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

from spdx.model.version import Version


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
