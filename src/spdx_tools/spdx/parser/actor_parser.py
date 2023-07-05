# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import re

from beartype.typing import Match, Pattern

from spdx_tools.spdx.model import Actor, ActorType
from spdx_tools.spdx.parser.error import SPDXParsingError
from spdx_tools.spdx.parser.parsing_functions import construct_or_raise_parsing_error


class ActorParser:
    @staticmethod
    def parse_actor(actor: str) -> Actor:
        tool_re: Pattern = re.compile(r"^Tool:\s*(.+)", re.UNICODE)
        person_re: Pattern = re.compile(r"^Person:\s*(?:(.*)\((.*)\)|(.*))$", re.UNICODE)
        org_re: Pattern = re.compile(r"^Organization:\s*(?:(.*)\((.*)\)|(.*))$", re.UNICODE)
        tool_match: Match = tool_re.match(actor)
        person_match: Match = person_re.match(actor)
        org_match: Match = org_re.match(actor)

        if tool_match:
            name: str = tool_match.group(1).strip()
            if not name:
                raise SPDXParsingError([f"No name for Tool provided: {actor}."])
            return construct_or_raise_parsing_error(Actor, dict(actor_type=ActorType.TOOL, name=name))

        if person_match:
            actor_type = ActorType.PERSON
            match = person_match
        elif org_match:
            actor_type = ActorType.ORGANIZATION
            match = org_match
        else:
            raise SPDXParsingError([f"Actor {actor} doesn't match any of person, organization or tool."])

        if match.group(3):
            return construct_or_raise_parsing_error(
                Actor, dict(actor_type=actor_type, name=match.group(3).strip(), email=None)
            )
        else:
            name = match.group(1)
            if not name:
                raise SPDXParsingError([f"No name for Actor provided: {actor}."])
            else:
                name = name.strip()

            email = match.group(2).strip()

            return construct_or_raise_parsing_error(
                Actor, dict(actor_type=actor_type, name=name, email=email if email else None)
            )
