# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0

from beartype.typing import List

from spdx_tools.spdx.model import Actor, ActorType
from spdx_tools.spdx.validation.validation_message import SpdxElementType, ValidationContext, ValidationMessage


def validate_actors(actors: List[Actor], parent_id: str) -> List[ValidationMessage]:
    validation_messages = []
    for actor in actors:
        validation_messages.extend(validate_actor(actor, parent_id))

    return validation_messages


def validate_actor(actor: Actor, parent_id: str) -> List[ValidationMessage]:
    validation_messages = []

    if actor.actor_type == ActorType.TOOL and actor.email is not None:
        validation_messages.append(
            ValidationMessage(
                f"email must be None if actor_type is TOOL, but is: {actor.email}",
                ValidationContext(parent_id=parent_id, element_type=SpdxElementType.ACTOR, full_element=actor),
            )
        )

    return validation_messages
