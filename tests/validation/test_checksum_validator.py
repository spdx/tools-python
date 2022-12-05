from typing import List

from src.model.checksum import Checksum, ChecksumAlgorithm
from src.validation.checksum_validator import ChecksumValidator
from src.validation.validation_message import ValidationMessage


def test_correct_checksum():
    checksum_validator = ChecksumValidator("2.3")

    checksum = Checksum(ChecksumAlgorithm.BLAKE2B_256, "value")
    validation_messages: List[ValidationMessage] = checksum_validator.validate_checksum(checksum)

    assert validation_messages == []
