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

from spdx3.model.agent import Agent
from spdx3.model.creation_information import CreationInformation
from spdx3.model.external_identifier import ExternalIdentifier, ExternalIdentifierType
from spdx3.model.organization import Organization
from spdx3.model.person import Person
from spdx3.model.software_agent import SoftwareAgent


@pytest.mark.parametrize("agent_class", [Agent, Person, Organization, SoftwareAgent])
def test_correct_initialization(agent_class):
    agent = agent_class("SPDXRef-Agent",
                        CreationInformation(Version("3.0.0"), datetime(2023, 1, 1), ["SPDXRef-Agent"], [], ["core"], "CC0"),
                        external_identifier=[ExternalIdentifier(ExternalIdentifierType.EMAIL, "some@mail.com")])

    assert agent.spdx_id == "SPDXRef-Agent"
    assert agent.creation_info == CreationInformation(Version("3.0.0"), datetime(2023, 1, 1), ["SPDXRef-Agent"], [],
                                                      ["core"], "CC0")
    assert agent.external_identifier == [ExternalIdentifier(ExternalIdentifierType.EMAIL, "some@mail.com")]


@pytest.mark.parametrize("agent_class", [Agent, Person, Organization, SoftwareAgent])
def test_invalid_initialization(agent_class):
    with pytest.raises(TypeError) as err:
        agent_class(12, 345)

    assert err.value.args[0] == [f'SetterError {agent_class.__name__}: type of argument "spdx_id" must be str; got int instead: 12',
                                 f'SetterError {agent_class.__name__}: type of argument "creation_info" must be '
                                 'spdx3.model.creation_information.CreationInformation; got int instead: 345']
