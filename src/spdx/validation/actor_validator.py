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

from typing import List

from spdx.model.actor import Actor, ActorType
from spdx.validation.validation_message import ValidationMessage, ValidationContext, SpdxElementType


def validate_actors(actors: List[Actor], parent_id: str) -> List[ValidationMessage]:
    validation_messages = []
    for actor in actors:
        validation_messages.extend(validate_actor(actor, parent_id))

    return validation_messages


def validate_actor(actor: Actor, parent_id: str) -> List[ValidationMessage]:
    validation_messages = []

    if actor.actor_type == ActorType.TOOL and actor.email is not None:
        validation_messages.append(
            ValidationMessage(
                f"email must be None if actor_type is TOOL, but is: {actor.email}",
                ValidationContext(parent_id=parent_id, element_type=SpdxElementType.ACTOR, full_element=actor)
            )
        )

    return validation_messages
