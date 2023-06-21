# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from enum import Enum, auto

from beartype.typing import Optional

from spdx_tools.common.typing.dataclass_with_properties import dataclass_with_properties
from spdx_tools.common.typing.type_checks import check_types_and_set_values


class ActorType(Enum):
    PERSON = auto()
    ORGANIZATION = auto()
    TOOL = auto()


@dataclass_with_properties
class Actor:
    actor_type: ActorType
    name: str
    email: Optional[str] = None

    def __init__(self, actor_type: ActorType, name: str, email: Optional[str] = None):
        check_types_and_set_values(self, locals())

    def to_serialized_string(self) -> str:
        """
        All serialization formats use the same representation of an actor, so this method is included in the data model
        """
        optional_email = f" ({self.email})" if self.email else ""
        return "".join([f"{self.actor_type.name.title()}:", f" {self.name}", optional_email])

    def __str__(self):
        return self.to_serialized_string()
