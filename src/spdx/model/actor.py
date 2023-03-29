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
from enum import Enum, auto
from typing import Optional

from common.typing.dataclass_with_properties import dataclass_with_properties
from common.typing.type_checks import check_types_and_set_values


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
