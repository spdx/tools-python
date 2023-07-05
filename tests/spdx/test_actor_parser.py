# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from unittest import TestCase

import pytest

from spdx_tools.spdx.model import ActorType
from spdx_tools.spdx.parser.actor_parser import ActorParser
from spdx_tools.spdx.parser.error import SPDXParsingError


@pytest.mark.parametrize(
    "actor_string,expected_type,expected_name,expected_mail",
    [
        ("Person: Jane Doe (jane.doe@example.com)", ActorType.PERSON, "Jane Doe", "jane.doe@example.com"),
        (
            "Organization: Example organization (organization@example.com)",
            ActorType.ORGANIZATION,
            "Example organization",
            "organization@example.com",
        ),
        ("Organization: Example organization ( )", ActorType.ORGANIZATION, "Example organization", None),
        ("Person: Example person ()", ActorType.PERSON, "Example person", None),
        ("Person: Example person ", ActorType.PERSON, "Example person", None),
        ("Tool: Example tool ", ActorType.TOOL, "Example tool", None),
        ("Tool: Example tool (email@mail.com)", ActorType.TOOL, "Example tool (email@mail.com)", None),
        (
            "Organization: (c) Chris Sainty (chris@sainty.com)",
            ActorType.ORGANIZATION,
            "(c) Chris Sainty",
            "chris@sainty.com",
        ),
    ],
)
def test_parse_actor(actor_string, expected_type, expected_name, expected_mail):
    actor_parser = ActorParser()

    actor = actor_parser.parse_actor(actor_string)

    assert actor.actor_type == expected_type
    assert actor.name == expected_name
    assert actor.email == expected_mail


@pytest.mark.parametrize(
    "actor_string,expected_message",
    [
        (
            "Perso: Jane Doe (jane.doe@example.com)",
            ["Actor Perso: Jane Doe (jane.doe@example.com) doesn't match any of person, organization or tool."],
        ),
        ("Toole Example Tool ()", ["Actor Toole Example Tool () doesn't match any of person, organization or tool."]),
        ("Organization:", ["No name for Actor provided: Organization:."]),
        ("Person: ( )", ["No name for Actor provided: Person: ( )."]),
    ],
)
def test_parse_invalid_actor(actor_string, expected_message):
    actor_parser = ActorParser()
    actor_string = actor_string

    with pytest.raises(SPDXParsingError) as err:
        actor_parser.parse_actor(actor_string)

    TestCase().assertCountEqual(err.value.get_messages(), expected_message)
