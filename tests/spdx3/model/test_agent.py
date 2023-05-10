# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from datetime import datetime

import pytest
from semantic_version import Version

from spdx_tools.spdx3.model import (
    Agent,
    CreationInformation,
    ExternalIdentifier,
    ExternalIdentifierType,
    Organization,
    Person,
    ProfileIdentifier,
    SoftwareAgent,
)


@pytest.mark.parametrize("agent_class", [Agent, Person, Organization, SoftwareAgent])
def test_correct_initialization(agent_class):
    agent = agent_class(
        "SPDXRef-Agent",
        CreationInformation(
            Version("3.0.0"), datetime(2023, 1, 1), ["SPDXRef-Agent"], [], [ProfileIdentifier.CORE], "CC0"
        ),
        external_identifier=[ExternalIdentifier(ExternalIdentifierType.EMAIL, "some@mail.com")],
    )

    assert agent.spdx_id == "SPDXRef-Agent"
    assert agent.creation_info == CreationInformation(
        Version("3.0.0"), datetime(2023, 1, 1), ["SPDXRef-Agent"], [], [ProfileIdentifier.CORE], "CC0"
    )
    assert agent.external_identifier == [ExternalIdentifier(ExternalIdentifierType.EMAIL, "some@mail.com")]


@pytest.mark.parametrize("agent_class", [Agent, Person, Organization, SoftwareAgent])
def test_invalid_initialization(agent_class):
    with pytest.raises(TypeError) as err:
        agent_class(12, 345)

    assert err.value.args[0] == [
        f'SetterError {agent_class.__name__}: type of argument "spdx_id" must be str; got int instead: ' "12",
        f'SetterError {agent_class.__name__}: type of argument "creation_info" must be '
        "spdx_tools.spdx3.model.creation_information.CreationInformation; got int "
        "instead: 345",
    ]
