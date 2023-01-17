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

from spdx3.model.spdx_collection import SpdxCollection


@mock.patch("spdx3.model.external_map.ExternalMap", autospec=True)
@mock.patch("spdx3.model.namespace_map.NamespaceMap", autospec=True)
@mock.patch("spdx3.model.element.Element", autospec=True)
@mock.patch("spdx3.model.creation_information.CreationInformation", autospec=True)
def test_correct_initialization(creation_information, element, namespace_map, external_map):
    spdx_collection = SpdxCollection("SPDXRef-Collection", creation_information, elements=[element],
                                     root_elements=[element], namespaces=[namespace_map], imports=[external_map])

    assert spdx_collection.spdx_id == "SPDXRef-Collection"
    assert spdx_collection.creation_info == creation_information
    assert spdx_collection.elements == [element]
    assert spdx_collection.root_elements == [element]
    assert spdx_collection.namespaces == [namespace_map]
    assert spdx_collection.imports == [external_map]


@mock.patch("spdx3.model.namespace_map.NamespaceMap", autospec=True)
@mock.patch("spdx3.model.creation_information.CreationInformation", autospec=True)
def test_invalid_initialization(creation_information, namespace_map):
    with pytest.raises(TypeError) as err:
        SpdxCollection("SPDXRef-Collection", creation_information, elements=[None], root_elements=3,
                       namespaces=namespace_map,
                       imports=["ExternalMap"])

    assert err.value.args[0] == ['SetterError SpdxCollection: type of argument "elements"[0] must be '
                                 'spdx3.model.element.Element; got NoneType instead: [None]',
                                 'SetterError SpdxCollection: type of argument "root_elements" must be a list; '
                                 'got int instead: 3',
                                 'SetterError SpdxCollection: type of argument "imports" must be one of '
                                 '(List[spdx3.model.external_map.ExternalMap], NoneType); got list instead: '
                                 "['ExternalMap']"]
