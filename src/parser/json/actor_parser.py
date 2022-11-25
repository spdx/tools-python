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
import re

from src.model.actor import Actor, ActorType
from src.model.spdx_no_assertion import SpdxNoAssertion
from src.model.typing.constructor_type_errors import ConstructorTypeErrors
from src.parser.error import SPDXParsingError

class ActorParser:

    def parse_actor(self, actor: str) -> Actor:
        tool_re = re.compile(r"Tool:\s*(.+)", re.UNICODE)
        person_re = re.compile(r"Person:\s*(([^(])+)(\((.*)\))?", re.UNICODE)
        org_re = re.compile(r"Organization:\s*(([^(])+)(\((.*)\))?", re.UNICODE)
        tool_match = tool_re.match(actor)
        person_match = person_re.match(actor)
        org_match = org_re.match(actor)

        if tool_match:
            name = tool_match.group(1).strip()
            try:
                creator = Actor(ActorType.TOOL, name=name)
            except ConstructorTypeErrors as err:
                raise SPDXParsingError(err.get_messages())
        elif person_match:
            name = person_match.group(1).strip()
            email = person_match.group(4).strip() if person_match.group(4) else None
            try:
                creator = Actor(ActorType.PERSON, name=name, email=email)
            except ConstructorTypeErrors as err:
                raise SPDXParsingError(err.get_messages())
        elif org_match:
            name = org_match.group(1).strip()
            email = org_match.group(4).strip() if org_match.group(4) else None
            try:
                creator = Actor(ActorType.ORGANIZATION, name=name, email=email)
            except ConstructorTypeErrors as err:
                raise SPDXParsingError(err.get_messages())

        else:
            raise SPDXParsingError([f"Actor {actor} doesn't match any of person, organization or tool."])

        return creator


    def parse_actor_or_no_assert(self, actor_or_no_assert: str):
        if actor_or_no_assert == SpdxNoAssertion.__str__:
            return SpdxNoAssertion()
        else:
            return self.parse_actor(actor_or_no_assert)
