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

import pytest

from spdx.model.actor import ActorType
from spdx.validation.actor_validator import validate_actor
from spdx.validation.validation_message import ValidationMessage, ValidationContext, SpdxElementType
from tests.spdx.fixtures import actor_fixture


def test_valid_actor_person():
    actor = actor_fixture()
    validation_messages: List[ValidationMessage] = validate_actor(actor, "SPDXRef-DOCUMENT")

    assert validation_messages == []


@pytest.mark.parametrize("actor, expected_message",
                         [(actor_fixture(actor_type=ActorType.TOOL, email="mail@mail.com"),
                           "email must be None if actor_type is TOOL, but is: mail@mail.com"),
                          ])
def test_invalid_actor(actor, expected_message):
    parent_id = "SPDXRef-DOCUMENT"
    validation_messages: List[ValidationMessage] = validate_actor(actor, parent_id)

    expected = ValidationMessage(expected_message,
                                 ValidationContext(parent_id=parent_id, element_type=SpdxElementType.ACTOR,
                                                   full_element=actor))

    assert validation_messages == [expected]
