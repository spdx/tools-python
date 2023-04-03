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

from spdx3.bump_from_spdx2.actor import bump_actor
from spdx3.model.creation_information import CreationInformation
from spdx3.model.external_identifier import ExternalIdentifier, ExternalIdentifierType
from spdx3.model.organization import Organization
from spdx3.model.person import Person
from spdx3.model.tool import Tool
from spdx3.payload import Payload
from spdx.model.actor import Actor, ActorType


@pytest.mark.parametrize(
    "actor_type, actor_name, actor_mail, element_type, new_spdx_id",
    [
        (ActorType.PERSON, "person name", "person@mail.com", Person, "SPDXRef-Actor-personname-person@mail.com"),
        (
            ActorType.ORGANIZATION,
            "organization name",
            "organization@mail.com",
            Organization,
            "SPDXRef-Actor-organizationname-organization@mail.com",
        ),
        (ActorType.TOOL, "tool name", None, Tool, "SPDXRef-Actor-toolname"),
    ],
)
def test_bump_actor(actor_type, actor_name, actor_mail, element_type, new_spdx_id):
    payload = Payload()
    document_namespace = "https://doc.namespace"
    creation_info = CreationInformation(Version("3.0.0"), datetime(2022, 1, 1), ["Creator"], [], ["core"])
    actor = Actor(actor_type, actor_name, actor_mail)

    agent_or_tool_id = bump_actor(actor, payload, creation_info, document_namespace)
    agent_or_tool = payload.get_element(agent_or_tool_id)

    assert isinstance(agent_or_tool, element_type)
    assert agent_or_tool.spdx_id == f"{document_namespace}#{new_spdx_id}"
    assert agent_or_tool.name == actor_name
    if actor_mail:
        assert len(agent_or_tool.external_identifier) == 1
        assert agent_or_tool.external_identifier[0] == ExternalIdentifier(ExternalIdentifierType.EMAIL, actor_mail)
    else:
        assert len(agent_or_tool.external_identifier) == 0


def test_bump_actor_that_already_exists():
    creation_info_old = CreationInformation(Version("3.0.0"), datetime(2022, 1, 1), ["Creator"], [], ["core"])
    creation_info_new = CreationInformation(Version("3.0.0"), datetime(2023, 2, 2), ["Creator"], [], ["core"])

    name = "some name"
    document_namespace = "https://doc.namespace"
    payload = Payload(
        {
            "https://doc.namespace#SPDXRef-Actor-somename-some@mail.com": Person(
                "https://doc.namespace#SPDXRef-Actor-somename-some@mail.com", creation_info_old, name
            )
        }
    )

    actor = Actor(ActorType.PERSON, name, "some@mail.com")
    agent_spdx_id = bump_actor(actor, payload, creation_info_new, document_namespace)

    # assert that there is only one Person in the payload
    assert (
        len(
            [
                payload.get_element(person_id)
                for person_id in payload.get_full_map()
                if isinstance(payload.get_element(person_id), Person)
            ]
        )
        == 1
    )
    assert payload.get_element(agent_spdx_id).creation_info == creation_info_old
