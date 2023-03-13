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
from datetime import datetime

import pytest
from semantic_version import Version

from spdx3.model.creation_information import CreationInformation
from spdx3.model.tool import Tool


def test_correct_initialization():
    agent = Tool("SPDXRef-Tool",
                 CreationInformation(Version("3.0.0"), datetime(2023, 1, 1), ["SPDXRef-Agent"], ["core"], "CC0"))

    assert agent.spdx_id == "SPDXRef-Tool"
    assert agent.creation_info == CreationInformation(Version("3.0.0"), datetime(2023, 1, 1), ["SPDXRef-Agent"],
                                                      ["core"], "CC0")


def test_invalid_initialization():
    with pytest.raises(TypeError) as err:
        Tool(12, 345)

    assert err.value.args[0] == ['SetterError Tool: type of argument "spdx_id" must be str; got int instead: 12',
                                 'SetterError Tool: type of argument "creation_info" must be '
                                 'spdx3.model.creation_information.CreationInformation; got int instead: 345']
