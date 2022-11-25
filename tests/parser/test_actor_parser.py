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

from src.model.actor import ActorType
from src.parser.error import SPDXParsingError
from src.parser.json.actor_parser import ActorParser


def test_actor_parser():
    actor_parser = ActorParser()
    actor_string = "Person: Jane Doe (jane.doe@example.com)"

    actor = actor_parser.parse_actor(actor_string)

    assert actor.actor_type == ActorType.PERSON
    assert actor.name == "Jane Doe"
    assert actor.email == "jane.doe@example.com"

def test_invalid_actor():
    actor_parser = ActorParser()
    actor_string = "Perso: Jane Doe (jane.doe@example.com)"

    with pytest.raises(SPDXParsingError) as err:
        _ = actor_parser.parse_actor(actor_string)
    assert err.typename == 'SPDXParsingError'
    assert err.value.messages[0] == "Actor Perso: Jane Doe (jane.doe@example.com) doesn't match any of person, organization or tool."
