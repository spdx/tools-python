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

from spdx3.model.artifact import Artifact


@mock.patch("spdx3.model.creation_information.CreationInformation", autospec=True)
def test_correct_initialization(creation_info):
    artifact = Artifact("SPDXRef-Artifact", creation_info, originated_by=None)

    assert artifact.spdx_id == "SPDXRef-Artifact"
    assert artifact.creation_info == creation_info
    assert artifact.originated_by is None


@mock.patch("spdx3.model.creation_information.CreationInformation", autospec=True)
def test_invalid_initialization(creation_info):
    with pytest.raises(TypeError) as err:
        Artifact(65, creation_info, originated_by=54)

    assert err.value.args[0] == ['SetterError Artifact: type of argument "spdx_id" must be str; got int '
                                 'instead: 65',
                                 'SetterError Artifact: type of argument "originated_by" must be NoneType; got '
                                 'int instead: 54']
