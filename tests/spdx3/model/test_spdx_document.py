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

from spdx3.model.spdx_document import SpdxDocument


@mock.patch("spdx3.model.element.Element", autospec=True)
@mock.patch("spdx3.model.creation_information.CreationInformation", autospec=True)
def test_correct_initialization(creation_information, element):
    spdx_document = SpdxDocument("SPDXRef-DOCUMENT", creation_information, "Test document", elements=[element],
                                 root_elements=[element])

    assert spdx_document.spdx_id == "SPDXRef-DOCUMENT"
    assert spdx_document.creation_info == creation_information
    assert spdx_document.name == "Test document"
    assert spdx_document.elements == [element]
    assert spdx_document.root_elements == [element]


def test_invalid_initialization():
    with pytest.raises(TypeError) as err:
        SpdxDocument(1, {"info": 5}, "document name", elements=[8], root_elements=[])

    assert err.value.args[0] == ['SetterError SpdxDocument: type of argument "spdx_id" must be str; got int '
                                 'instead: 1',
                                 'SetterError SpdxDocument: type of argument "creation_info" must be '
                                 'spdx3.model.creation_information.CreationInformation; got dict instead: '
                                 "{'info': 5}",
                                 'SetterError SpdxDocument: type of argument "elements"[0] must be '
                                 'spdx3.model.element.Element; got int instead: [8]']


@mock.patch("spdx3.model.creation_information.CreationInformation", autospec=True)
def test_incomplete_initialization(creation_information):
    with pytest.raises(TypeError) as err:
        SpdxDocument("SPDXRef-Docuement", creation_information)

    assert err.value.args[
               0] == "SpdxDocument.__init__() missing 3 required positional arguments: 'name', 'elements', and 'root_elements'"
