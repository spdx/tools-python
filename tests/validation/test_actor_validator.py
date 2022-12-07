from typing import List

import pytest

from src.model.actor import ActorType, Actor
from src.validation.actor_validator import ActorValidator
from src.validation.validation_message import ValidationMessage, ValidationContext, SpdxElementType
from tests.valid_defaults import get_actor


def test_correct_actor_person():
    actor_validator = ActorValidator("2.3", "SPDXRef-DOCUMENT")

    actor = Actor(ActorType.PERSON, "person name", "mail@mail.com")
    validation_messages: List[ValidationMessage] = actor_validator.validate_actor(actor)

    assert validation_messages == []


@pytest.mark.parametrize("actor_input, expected_message",
                         [(get_actor(actor_type=ActorType.TOOL, mail="mail@mail.com"),
                           f"email must be None if actor_type is TOOL, but is mail@mail.com"),
                          ])
def test_wrong_actor(actor_input, expected_message):
    parent_id = "SPDXRef-Document"
    actor_validator = ActorValidator("2.3", parent_id)
    actor = actor_input
    validation_messages: List[ValidationMessage] = actor_validator.validate_actor(actor)

    expected = ValidationMessage(expected_message,
                                 ValidationContext(parent_id=parent_id, element_type=SpdxElementType.ACTOR,
                                                   full_element=actor))

    assert validation_messages == [expected]
