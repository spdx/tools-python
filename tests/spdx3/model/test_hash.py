# Copyright (c) 2023 spdx contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#    http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import pytest

from spdx3.model.hash import Hash, HashAlgorithm


def test_correct_initialization():
    hash = Hash(algorithm=HashAlgorithm.SHA1, hash_value="value")

    assert hash.algorithm == HashAlgorithm.SHA1
    assert hash.hash_value == "value"


def test_invalid_initialization():
    with pytest.raises(TypeError) as err:
        Hash("SHA1", 345)

    assert err.value.args[0] == [
        'SetterError Hash: type of argument "algorithm" must be '
        "spdx3.model.hash.HashAlgorithm; got str instead: SHA1",
        'SetterError Hash: type of argument "hash_value" must be str; got int ' "instead: 345",
    ]
