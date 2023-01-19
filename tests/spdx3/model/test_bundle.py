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
from unittest import mock

import pytest

from spdx3.model.bundle import Bundle


@mock.patch("spdx3.model.namespace_map.NamespaceMap", autospec=True)
@mock.patch("spdx3.model.creation_information.CreationInformation", autospec=True)
def test_correct_initialization(creation_information, namespace):
    bundle = Bundle("SPDXRef-Bundle", creation_information, elements=["spdx_id1"], root_elements=["spdx_id2"],
                    namespaces=[namespace], context="context")

    assert bundle.spdx_id == "SPDXRef-Bundle"
    assert bundle.creation_info == creation_information
    assert bundle.elements == ["spdx_id1"]
    assert bundle.root_elements == ["spdx_id2"]
    assert bundle.context == "context"
    assert bundle.namespaces == [namespace]


@mock.patch("spdx3.model.creation_information.CreationInformation", autospec=True)
def test_invalid_initialization(creation_information):
    with pytest.raises(TypeError) as err:
        Bundle(4, creation_information, elements="spdx_id1", root_elements=[42], namespaces=True, context=["yes"])

    assert err.value.args[0] == ['SetterError Bundle: type of argument "spdx_id" must be str; got int instead: 4',
                                 'SetterError Bundle: type of argument "elements" must be a list; got str '
                                 'instead: spdx_id1',
                                 'SetterError Bundle: type of argument "root_elements"[0] must be str; got int '
                                 'instead: [42]',
                                 'SetterError Bundle: type of argument "namespaces" must be one of '
                                 '(List[spdx3.model.namespace_map.NamespaceMap], NoneType); got bool instead: True',
                                 'SetterError Bundle: type of argument "context" must be one of (str, '
                                 "NoneType); got list instead: ['yes']"]
