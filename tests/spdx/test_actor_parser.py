# Copyright (c) 2022 spdx contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import pytest
from unittest import TestCase

from spdx.model.actor import ActorType
from spdx.parser.error import SPDXParsingError
from spdx.parser.actor_parser import ActorParser


@pytest.mark.parametrize("actor_string,expected_type,expected_name,expected_mail", [
    ("Person: Jane Doe (jane.doe@example.com)", ActorType.PERSON, "Jane Doe", "jane.doe@example.com"),
    ("Organization: Example organization (organization@example.com)", ActorType.ORGANIZATION, "Example organization",
     "organization@example.com"),
    ("Organization: Example organization ( )", ActorType.ORGANIZATION, "Example organization", None),
    ("Tool: Example tool ", ActorType.TOOL, "Example tool", None)])
def test_parse_actor(actor_string, expected_type, expected_name, expected_mail):
    actor_parser = ActorParser()

    actor = actor_parser.parse_actor(actor_string)

    assert actor.actor_type == expected_type
    assert actor.name == expected_name
    assert actor.email == expected_mail


@pytest.mark.parametrize("actor_string,expected_message", [
    ("Perso: Jane Doe (jane.doe@example.com)",
     ["Actor Perso: Jane Doe (jane.doe@example.com) doesn't match any of person, organization or tool."]),
    ("Toole Example Tool ()",
     ["Actor Toole Example Tool () doesn't match any of person, organization or tool."])
])
def test_parse_invalid_actor(actor_string, expected_message):
    actor_parser = ActorParser()
    actor_string = actor_string

    with pytest.raises(SPDXParsingError) as err:
        actor_parser.parse_actor(actor_string)

    TestCase().assertCountEqual(err.value.get_messages(), expected_message)
