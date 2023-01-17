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

from spdx3.model.element import Element, Artifact, SpdxCollection, Bundle, Bom


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
def test_correct_initialization_spdx_collection(creation_information, namespace_map, external_map):
    element = Element("SPDXRef-Element",
                      creation_info=creation_information)  # using a mock here leads to failure as check_types_and_set_values accesses the element class
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
def test_invalid_initialization_spdx_collection(creation_information, namespace_map):
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


@mock.patch("spdx3.model.namespace_map.NamespaceMap", autospec=True)
@mock.patch("spdx3.model.creation_information.CreationInformation", autospec=True)
def test_correct_initialization_bundle(creation_information, namespace):
    element = Element("SPDXRef-Element",
                      creation_info=creation_information)  # using a mock here leads to failure as check_types_and_set_values accesses the element class
    bundle = Bundle("SPDXRef-Bundle", creation_information, elements=[element], root_elements=[element],
                    namespaces=[namespace], context="context")

    assert bundle.spdx_id == "SPDXRef-Bundle"
    assert bundle.creation_info == creation_information
    assert bundle.elements == [element]
    assert bundle.root_elements == [element]
    assert bundle.context == "context"
    assert bundle.namespaces == [namespace]


@mock.patch("spdx3.model.creation_information.CreationInformation", autospec=True)
def test_invalid_initialization_bundle(creation_information):
    element = Element("SPDXRef-Element",
                      creation_info=creation_information)  # using a mock here leads to failure as check_types_and_set_values accesses the element class
    with pytest.raises(TypeError) as err:
        Bundle(4, creation_information, elements=[element], root_elements=[element], namespaces=True, context=["yes"])

    assert err.value.args[0] == ['SetterError Bundle: type of argument "spdx_id" must be str; got int instead: '
                                 '4',
                                 'SetterError Bundle: type of argument "namespaces" must be one of '
                                 '(List[spdx3.model.namespace_map.NamespaceMap], NoneType); got bool instead: True',
                                 'SetterError Bundle: type of argument "context" must be one of (str, '
                                 "NoneType); got list instead: ['yes']"]


@mock.patch("spdx3.model.creation_information.CreationInformation", autospec=True)
def test_correct_initialization_bom(creation_information):
    element = Element("SPDXRef-Element",
                      creation_info=creation_information)  # using a mock here leads to failure as check_types_and_set_values accesses the element class
    bom = Bom("SPDXRef-Bom", creation_information, elements=[element], root_elements=[element])

    assert bom.spdx_id == "SPDXRef-Bom"
    assert bom.creation_info == creation_information
    assert bom.elements == [element]
    assert bom.root_elements == [element]


def test_invalid_initialization_bom():
    with pytest.raises(TypeError) as err:
        Bom(1, "Creation Information", elements=[5], root_elements=[])

    assert err.value.args[0] == ['SetterError Bom: type of argument "spdx_id" must be str; got int instead: 1',
                                 'SetterError Bom: type of argument "creation_info" must be '
                                 'spdx3.model.creation_information.CreationInformation; got str instead: '
                                 'Creation Information',
                                 'SetterError Bom: type of argument "elements"[0] must be '
                                 'spdx3.model.element.Element; got int instead: [5]']
