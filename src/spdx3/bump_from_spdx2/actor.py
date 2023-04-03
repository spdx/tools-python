# Copyright (c) 2023 spdx contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from typing import List

from spdx3.model.creation_information import CreationInformation
from spdx3.model.external_identifier import ExternalIdentifier, ExternalIdentifierType
from spdx3.model.organization import Organization
from spdx3.model.person import Person
from spdx3.model.tool import Tool
from spdx3.payload import Payload
from spdx.model.actor import Actor as Spdx2_Actor
from spdx.model.actor import ActorType


def bump_actor(
    spdx2_actor: Spdx2_Actor, payload: Payload, creation_info: CreationInformation, document_namespace: str
) -> str:
    name: str = spdx2_actor.name
    email: str = spdx2_actor.email
    actor_type: ActorType = spdx2_actor.actor_type

    external_identifiers: List[ExternalIdentifier] = []
    name_without_whitespace = "".join(name.split())
    if email:
        external_identifiers.append(ExternalIdentifier(ExternalIdentifierType.EMAIL, email))
        spdx_id: str = f"{document_namespace}#SPDXRef-Actor-{name_without_whitespace}-{email}"
    else:
        spdx_id: str = f"{document_namespace}#SPDXRef-Actor-{name_without_whitespace}"

    if spdx_id in payload.get_full_map():  # the agent/tool already exists, so we don't need to create a new one
        return spdx_id

    if actor_type == ActorType.PERSON:
        agent_or_tool = Person(
            spdx_id=spdx_id, creation_info=creation_info, name=name, external_identifier=external_identifiers
        )

    elif actor_type == ActorType.ORGANIZATION:
        agent_or_tool = Organization(
            spdx_id=spdx_id, creation_info=creation_info, name=name, external_identifier=external_identifiers
        )

    elif actor_type == ActorType.TOOL:
        agent_or_tool = Tool(
            spdx_id=spdx_id, creation_info=creation_info, name=name, external_identifier=external_identifiers
        )

    else:
        raise ValueError(f"no conversion rule defined for ActorType {actor_type}")

    payload.add_element(agent_or_tool)

    return spdx_id
