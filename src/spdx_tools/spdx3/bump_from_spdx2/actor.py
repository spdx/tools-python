# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from typing import Optional

from beartype.typing import List

from spdx_tools.spdx3.model import CreationInfo, ExternalIdentifier, ExternalIdentifierType, Organization, Person, Tool
from spdx_tools.spdx3.payload import Payload
from spdx_tools.spdx.model.actor import Actor as Spdx2_Actor
from spdx_tools.spdx.model.actor import ActorType


def bump_actor(
    spdx2_actor: Spdx2_Actor, payload: Payload, document_namespace: str, creation_info: Optional[CreationInfo] = None
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

    value_dict = {
        "spdx_id": spdx_id,
        "creation_info": creation_info,
        "name": name,
        "external_identifier": external_identifiers,
    }

    if actor_type == ActorType.PERSON:
        agent_or_tool = Person(**value_dict)

    elif actor_type == ActorType.ORGANIZATION:
        agent_or_tool = Organization(**value_dict)

    elif actor_type == ActorType.TOOL:
        agent_or_tool = Tool(**value_dict)

    else:
        raise ValueError(f"no conversion rule defined for ActorType {actor_type}")

    payload.add_element(agent_or_tool)

    return spdx_id
