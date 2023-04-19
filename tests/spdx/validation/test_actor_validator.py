# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0

from typing import List

import pytest

from spdx_tools.spdx.constants import DOCUMENT_SPDX_ID
from spdx_tools.spdx.model import ActorType
from spdx_tools.spdx.validation.actor_validator import validate_actor
from spdx_tools.spdx.validation.validation_message import SpdxElementType, ValidationContext, ValidationMessage
from tests.spdx.fixtures import actor_fixture


def test_valid_actor_person():
    actor = actor_fixture()
    validation_messages: List[ValidationMessage] = validate_actor(actor, DOCUMENT_SPDX_ID)

    assert validation_messages == []


@pytest.mark.parametrize(
    "actor, expected_message",
    [
        (
            actor_fixture(actor_type=ActorType.TOOL, email="mail@mail.com"),
            "email must be None if actor_type is TOOL, but is: mail@mail.com",
        ),
    ],
)
def test_invalid_actor(actor, expected_message):
    parent_id = DOCUMENT_SPDX_ID
    validation_messages: List[ValidationMessage] = validate_actor(actor, parent_id)

    expected = ValidationMessage(
        expected_message,
        ValidationContext(parent_id=parent_id, element_type=SpdxElementType.ACTOR, full_element=actor),
    )

    assert validation_messages == [expected]
