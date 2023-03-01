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
from typing import Pattern, Match, Optional

from spdx.model.actor import Actor, ActorType
from spdx.parser.error import SPDXParsingError
from spdx.parser.parsing_functions import construct_or_raise_parsing_error


class ActorParser:

    @staticmethod
    def parse_actor(actor: str) -> Actor:
        tool_re: Pattern = re.compile(r"^Tool:\s*(.+)", re.UNICODE)
        person_re: Pattern = re.compile(r"^Person:\s*(([^(])+)(\((.*)\))?", re.UNICODE)
        org_re: Pattern = re.compile(r"^Organization:\s*(([^(])+)(\((.*)\))?", re.UNICODE)
        tool_match: Match = tool_re.match(actor)
        person_match: Match = person_re.match(actor)
        org_match: Match = org_re.match(actor)

        if tool_match:
            name: str = tool_match.group(1).strip()
            if not name:
                raise SPDXParsingError([f"No name for Tool provided: {actor}."])
            creator = construct_or_raise_parsing_error(Actor, dict(actor_type=ActorType.TOOL, name=name))

        elif person_match:
            name: str = person_match.group(1).strip()
            if not name:
                raise SPDXParsingError([f"No name for Person provided: {actor}."])
            email: Optional[str] = ActorParser.get_email_or_none(person_match)
            creator = construct_or_raise_parsing_error(Actor, dict(actor_type=ActorType.PERSON, name=name, email=email))
        elif org_match:
            name: str = org_match.group(1).strip()
            if not name:
                raise SPDXParsingError([f"No name for Organization provided: {actor}."])
            email: Optional[str] = ActorParser.get_email_or_none(org_match)
            creator = construct_or_raise_parsing_error(Actor,
                                                       dict(actor_type=ActorType.ORGANIZATION, name=name, email=email))
        else:
            raise SPDXParsingError([f"Actor {actor} doesn't match any of person, organization or tool."])

        return creator

    @staticmethod
    def get_email_or_none(match: Match) -> Optional[str]:
        email_match = match.group(4)
        if email_match and email_match.strip():
            email = email_match.strip()
        else:
            email = None
        return email
