from datetime import datetime
from typing import List
from unittest import mock

from src.model.document import CreationInfo
from src.model.version import Version
from src.validation.creation_info_validator import CreationInfoValidator
from src.validation.validation_message import ValidationMessage


@mock.patch('src.model.actor.Actor', autospec=True)
def test_correct_creation_info(actor):
    creation_info_validator = CreationInfoValidator("2.3")

    creation_info = CreationInfo([actor, actor], datetime(2022, 1, 1), "comment", Version(6, 3))
    validation_messages: List[ValidationMessage] = creation_info_validator.validate_creation_info(creation_info)

    assert validation_messages == []
