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


class ActorType(Enum):
    PERSON = auto()
    ORGANIZATION = auto()
    TOOL = auto()


class Actor:
    actor_type: ActorType
    name: str
    email: Optional[str]

    def __init__(self, actor_type: ActorType, name: str, email: Optional[str] = None):
        self.actor_type = actor_type
        self.name = name
        self.email = email
