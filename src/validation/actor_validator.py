from typing import List

from src.model.actor import Actor
from src.validation.validation_message import ValidationMessage


class ActorValidator:
    spdx_version: str

    def __init__(self, spdx_version):
        self.spdx_version = spdx_version

    def validate_actors(self, actors: List[Actor]) -> List[ValidationMessage]:
        error_messages = []
        for actor in actors:
            error_messages.extend(self.validate_actor(actor))

        return error_messages

    def validate_actor(self, actor: Actor) -> List[ValidationMessage]:
        pass
