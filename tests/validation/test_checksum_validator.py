from typing import List
import pytest
from src.model.checksum import Checksum, ChecksumAlgorithm
from src.validation.checksum_validator import ChecksumValidator
from src.validation.validation_message import ValidationMessage, ValidationContext, SpdxElementType
from tests.valid_defaults import get_checksum


# TODO: add positive tests for all algorithms
def test_correct_checksum():
    checksum_validator = ChecksumValidator("2.3", "parent_id")

    checksum = Checksum(ChecksumAlgorithm.SHA1, "85ed0817af83a24ad8da68c2b5094de69833983c")
    validation_messages: List[ValidationMessage] = checksum_validator.validate_checksum(checksum)

    assert validation_messages == []


# TODO: add negative tests for all algorithms
@pytest.mark.parametrize("checksum, expected_message",
                         [(get_checksum(algorithm=ChecksumAlgorithm.SHA1, value="invalid_value"),
                           'value of ChecksumAlgorithm.SHA1 must consist of 40 hexadecimal digits, but is: invalid_value (length: 13 digits)'),
                          ])
def test_wrong_checksum(checksum, expected_message):
    parent_id = "parent_id"
    checksum_validator = ChecksumValidator("2.3", parent_id)
    validation_messages: List[ValidationMessage] = checksum_validator.validate_checksum(checksum)

    expected = ValidationMessage(expected_message,
                                 ValidationContext(parent_id=parent_id, element_type=SpdxElementType.CHECKSUM,
                                                   full_element=checksum))

    assert validation_messages == [expected]
