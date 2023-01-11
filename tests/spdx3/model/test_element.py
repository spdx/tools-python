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
from unittest import mock

import pytest

from spdx3.model.element import Element, Artifact, Collection, Bundle, Bom


@mock.patch("spdx3.model.creation_information.CreationInformation")
def test_correct_initialization_element(creation_info):
    element = Element("SPDXRef-Element", creation_info)

    assert element.spdx_id == "SPDXRef-Element"
    assert element.creation_info == creation_info


@mock.patch("spdx3.model.creation_information.CreationInformation", autospec=True)
def test_invalid_initialization_element(creation_info):
    with pytest.raises(TypeError) as err:
        Element(54, creation_info, name=76)

    assert err.value.args[0] == ['SetterError Element: type of argument "spdx_id" must be str; got int '
                                 'instead: 54',
                                 'SetterError Element: type of argument "name" must be one of (str, NoneType); '
                                 'got int instead: 76']


@mock.patch("spdx3.model.creation_information.CreationInformation", autospec=True)
def test_correct_initialization_artifact(creation_info):
    artifact = Artifact("SPDXRef-Artifact", creation_info, originated_by=None)

    assert artifact.spdx_id == "SPDXRef-Artifact"
    assert artifact.creation_info == creation_info
    assert artifact.originated_by is None


@mock.patch("spdx3.model.creation_information.CreationInformation", autospec=True)
def test_invalid_initialization_artifact(creation_info):
    with pytest.raises(TypeError) as err:
        Artifact(65, creation_info, originated_by=54)

    assert err.value.args[0] == ['SetterError Artifact: type of argument "spdx_id" must be str; got int '
                                 'instead: 65',
                                 'SetterError Artifact: type of argument "originated_by" must be NoneType; got '
                                 'int instead: 54']


@mock.patch("spdx3.model.external_map.ExternalMap", autospec=True)
@mock.patch("spdx3.model.namespace_map.NamespaceMap", autospec=True)
@mock.patch("spdx3.model.creation_information.CreationInformation", autospec=True)
def test_correct_initialization_collection(creation_information, namespace_map, external_map):
    collection = Collection("SPDXRef-Collection", creation_information, namespace=namespace_map,
                            import_element=[external_map])

    assert collection.spdx_id == "SPDXRef-Collection"
    assert collection.creation_info == creation_information
    assert collection.namespace == namespace_map
    assert collection.import_element == [external_map]


@mock.patch("spdx3.model.namespace_map.NamespaceMap", autospec=True)
@mock.patch("spdx3.model.creation_information.CreationInformation", autospec=True)
def test_invalid_initialization_collection(creation_information, namespace_map):
    with pytest.raises(TypeError) as err:
        Collection("SPDXRef-Collection", creation_information, namespace=namespace_map,
                   import_element=["ExternalMap"])

    assert err.value.args[0] == ['SetterError Collection: type of argument "import_element" must be one of '
                                 '(List[spdx3.model.external_map.ExternalMap], NoneType); got list instead: '
                                 "['ExternalMap']"]


@mock.patch("spdx3.model.namespace_map.NamespaceMap", autospec=True)
@mock.patch("spdx3.model.creation_information.CreationInformation", autospec=True)
def test_correct_initialization_bundle(creation_information, namespace):
    bundle = Bundle("SPDXRef-Bundle", creation_information, namespace=namespace, context="context")

    assert bundle.spdx_id == "SPDXRef-Bundle"
    assert bundle.creation_info == creation_information
    assert bundle.context == "context"
    assert bundle.namespace == namespace


@mock.patch("spdx3.model.creation_information.CreationInformation", autospec=True)
def test_invalid_initialization_bundle(creation_information):
    with pytest.raises(TypeError) as err:
        Bundle(4, creation_information, namespace=True, context=["yes"])

    assert err.value.args[0] == ['SetterError Bundle: type of argument "spdx_id" must be str; got int instead: '
                                 '4',
                                 'SetterError Bundle: type of argument "namespace" must be one of '
                                 '(spdx3.model.namespace_map.NamespaceMap, NoneType); got bool instead: True',
                                 'SetterError Bundle: type of argument "context" must be one of (str, '
                                 "NoneType); got list instead: ['yes']"]


@mock.patch("spdx3.model.creation_information.CreationInformation", autospec=True)
def test_correct_initialization_bom(creation_information):
    bom = Bom("SPDXRef-Bom", creation_information)

    assert bom.spdx_id == "SPDXRef-Bom"
    assert bom.creation_info == creation_information


def test_invalid_initialization_bom():
    with pytest.raises(TypeError) as err:
        Bom(1, "Creation Information")

    assert err.value.args[0] == ['SetterError Bom: type of argument "spdx_id" must be str; got int instead: 1',
                                 'SetterError Bom: type of argument "creation_info" must be '
                                 'spdx3.model.creation_information.CreationInformation; got str instead: '
                                 'Creation Information']
