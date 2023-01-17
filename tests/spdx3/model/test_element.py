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
