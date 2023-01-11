# Copyright (c) 2023 spdx contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#   http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import pytest

from spdx3.model.namespace_map import NamespaceMap


def test_correct_initialization():
    namespace_map = NamespaceMap("some prefix", "https://namespace")

    assert namespace_map.prefix == "some prefix"
    assert namespace_map.namespace == "https://namespace"


def test_invalid_initialization():
    with pytest.raises(TypeError) as err:
        NamespaceMap(34, ["list of namespaces"])

    assert err.value.args[0] == ['SetterError NamespaceMap: type of argument "prefix" must be one of (str, '
                                 'NoneType); got int instead: 34',
                                 'SetterError NamespaceMap: type of argument "namespace" must be one of (str, '
                                 "NoneType); got list instead: ['list of namespaces']"]
