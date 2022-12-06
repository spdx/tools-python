from typing import List

from src.model.actor import Actor, ActorType
from src.validation.actor_validator import ActorValidator
from src.validation.validation_message import ValidationMessage, ValidationContext, SpdxElementType


def test_correct_actor():
    actor_validator = ActorValidator("2.3")

    actor = Actor(ActorType.TOOL, "tool_name", "mail")
    validation_messages: List[ValidationMessage] = actor_validator.validate_actor(actor)

    assert validation_messages == []
