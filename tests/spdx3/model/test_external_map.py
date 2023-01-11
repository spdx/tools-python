# Copyright (c) 2023 spdx contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#  http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import pytest

from spdx3.model.external_map import ExternalMap


def test_correct_initialization():
    external_map = ExternalMap("https://external.id", None, "https://location.hint")

    assert external_map.external_id == "https://external.id"
    assert external_map.verified_using is None
    assert external_map.location_hint == "https://location.hint"


def test_invalid_initialization():
    with pytest.raises(TypeError) as err:
        ExternalMap(234, None, ["location  hints"])

    assert err.value.args[0] == ['SetterError ExternalMap: type of argument "external_id" must be str; got int '
                                 'instead: 234',
                                 'SetterError ExternalMap: type of argument "location_hint" must be one of '
                                 "(str, NoneType); got list instead: ['location  hints']"]
