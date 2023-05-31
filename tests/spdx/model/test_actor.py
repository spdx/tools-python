# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0

import pytest

from spdx_tools.spdx.model import Actor, ActorType


def test_correct_initialization():
    actor = Actor(ActorType.TOOL, "tool_name", "mail")
    assert actor.actor_type == ActorType.TOOL
    assert actor.name == "tool_name"
    assert actor.email == "mail"


def test_correct_initialization_with_optional_as_none():
    actor = Actor(ActorType.TOOL, "tool_name")
    assert actor.actor_type == ActorType.TOOL
    assert actor.name == "tool_name"
    assert actor.email is None


@pytest.mark.parametrize(
    "actor,expected_string",
    [
        (Actor(ActorType.PERSON, "personName"), "Person: personName"),
        (Actor(ActorType.PERSON, "personName", "personEmail"), "Person: personName (personEmail)"),
        (Actor(ActorType.ORGANIZATION, "orgName"), "Organization: orgName"),
        (Actor(ActorType.ORGANIZATION, "orgName", "orgEmail"), "Organization: orgName (orgEmail)"),
        (Actor(ActorType.TOOL, "toolName"), "Tool: toolName"),
        (Actor(ActorType.TOOL, "toolName", "toolEmail"), "Tool: toolName (toolEmail)"),
    ],
)
def test_serialization(actor: Actor, expected_string: str):
    assert actor.to_serialized_string() == expected_string
