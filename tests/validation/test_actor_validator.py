from typing import List

import pytest

from src.model.actor import ActorType, Actor
from src.validation.actor_validator import validate_actor
from src.validation.validation_message import ValidationMessage, ValidationContext, SpdxElementType
from tests.valid_defaults import get_actor


def test_valid_actor_person():
    actor = Actor(ActorType.PERSON, "person name", "mail@mail.com")
    validation_messages: List[ValidationMessage] = validate_actor(actor, "SPDXRef-DOCUMENT")

    assert validation_messages == []


@pytest.mark.parametrize("actor, expected_message",
                         [(get_actor(actor_type=ActorType.TOOL, mail="mail@mail.com"),
                           "email must be None if actor_type is TOOL, but is: mail@mail.com"),
                          ])
def test_invalid_actor(actor, expected_message):
    parent_id = "SPDXRef-DOCUMENT"
    validation_messages: List[ValidationMessage] = validate_actor(actor, parent_id)

    expected = ValidationMessage(expected_message,
                                 ValidationContext(parent_id=parent_id, element_type=SpdxElementType.ACTOR,
                                                   full_element=actor))

    assert validation_messages == [expected]
