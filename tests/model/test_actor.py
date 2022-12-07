import pytest

from src.model.actor import Actor, ActorType


def test_correct_initialization():
    actor = Actor(ActorType.TOOL, "tool_name", "mail")
    assert actor.actor_type == ActorType.TOOL
    assert actor.name == "tool_name"
    assert actor.email == "mail"


def test_correct_initialization_with_optional_as_none():
    actor = Actor(ActorType.TOOL, "tool_name", None)
    assert actor.actor_type == ActorType.TOOL
    assert actor.name == "tool_name"
    assert actor.email is None


def test_wrong_type_in_actor_type():
    with pytest.raises(TypeError):
        Actor("PERSON", "name")


def test_wrong_type_in_name():
    with pytest.raises(TypeError):
        Actor(ActorType.PERSON, 42)


def test_wrong_type_in_email():
    with pytest.raises(TypeError):
        Actor(ActorType.PERSON, "name", [])


def test_wrong_type_in_email_after_initializing():
    with pytest.raises(TypeError):
        actor = Actor(ActorType.PERSON, "name")
        actor.email = []

def test():
    Actor("string", 2, [])
