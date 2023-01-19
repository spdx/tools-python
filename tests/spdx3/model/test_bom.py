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

from spdx3.model.bom import Bom


@mock.patch("spdx3.model.creation_information.CreationInformation", autospec=True)
def test_correct_initialization(creation_information):
    bom = Bom("SPDXRef-Bom", creation_information, elements=["spdx_id1"], root_elements=["spdx_id2"])

    assert bom.spdx_id == "SPDXRef-Bom"
    assert bom.creation_info == creation_information
    assert bom.elements == ["spdx_id1"]
    assert bom.root_elements == ["spdx_id2"]


def test_invalid_initialization():
    with pytest.raises(TypeError) as err:
        Bom(1, "Creation Information", elements=[5], root_elements=[])

    assert err.value.args[0] == ['SetterError Bom: type of argument "spdx_id" must be str; got int instead: 1',
                                 'SetterError Bom: type of argument "creation_info" must be '
                                 'spdx3.model.creation_information.CreationInformation; got str instead: '
                                 'Creation Information',
                                 'SetterError Bom: type of argument "elements"[0] must be '
                                 'str; got int instead: [5]']
