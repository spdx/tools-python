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
from spdx3.model.element import Element

from spdx3.model.software.sbom import Sbom


@mock.patch("spdx3.model.creation_information.CreationInformation", autospec=True)
def test_correct_initialization_sbom(creation_information):
    element = Element("SPDXRef-Element",
                      creation_info=creation_information)  # using a mock here leads to failure as check_types_and_set_values accesses the element class

    sbom = Sbom("SPDXRef-Sbom", creation_information, elements=[element, element], root_elements=[element])

    assert sbom.spdx_id == "SPDXRef-Sbom"
    assert sbom.creation_info == creation_information
    assert sbom.elements == [element, element]
    assert sbom.root_elements == [element]

def test_invalid_initialization_sbom():
    with pytest.raises(TypeError) as err:
        Sbom(2, {"creation_info": [3, 4, 5]}, elements=[], root_elements=[])

    assert err.value.args[0] == ['SetterError Sbom: type of argument "spdx_id" must be str; got int instead: 2',
                                 'SetterError Sbom: type of argument "creation_info" must be '
                                 'spdx3.model.creation_information.CreationInformation; got dict instead: '
                                 "{'creation_info': [3, 4, 5]}"]
