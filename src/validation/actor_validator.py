from typing import List, Optional

from src.model.actor import Actor, ActorType
from src.validation.validation_message import ValidationMessage, ValidationContext, SpdxElementType


class ActorValidator:
    spdx_version: str
    parent_id: str

    def __init__(self, spdx_version: str, parent_id: Optional[str]):
        self.spdx_version = spdx_version
        self.parent_id = parent_id

    def validate_actors(self, actors: List[Actor]) -> List[ValidationMessage]:
        validation_messages = []
        for actor in actors:
            validation_messages.extend(self.validate_actor(actor))

        return validation_messages

    def validate_actor(self, actor: Actor) -> List[ValidationMessage]:
        validation_messages = []

        if actor.actor_type == ActorType.TOOL and actor.email is not None:
            validation_messages.append(
                ValidationMessage(
                    f"email must be None if actor_type is TOOL, but is: {actor.email}",
                    ValidationContext(parent_id=self.parent_id, element_type=SpdxElementType.ACTOR, full_element=actor)
                )
            )

        return validation_messages
