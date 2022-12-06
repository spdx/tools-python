from typing import List
from unittest import mock

from src.model.file import File, FileType
from src.model.spdx_no_assertion import SpdxNoAssertion
from src.model.spdx_none import SpdxNone
from src.validation.file_validator import FileValidator
from src.validation.validation_message import ValidationMessage, ValidationContext, SpdxElementType


@mock.patch('src.model.checksum.Checksum', autospec=True)
def test_correct_file(checksum):
    file_validator = FileValidator("2.3")

    file = File("name", "id", [checksum, checksum], [FileType.OTHER, FileType.SPDX], SpdxNone(), SpdxNoAssertion(),
                "comment on license", "copyright", "comment", "notice", ["contributor"], ["attribution"])
    validation_messages: List[ValidationMessage] = file_validator.validate_file(file)

    assert validation_messages == []
