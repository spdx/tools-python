from typing import List

from src.model.checksum import Checksum
from src.validation.validation_message import ValidationMessage


class ChecksumValidator:
    spdx_version: str

    def __init__(self, spdx_version):
        self.spdx_version = spdx_version

    def validate_checksums(self, checksums: List[Checksum]) -> List[ValidationMessage]:
        error_messages = []
        for checksum in checksums:
            error_messages.extend(self.validate_checksum(checksum))

        return error_messages

    def validate_checksum(self, checksum: Checksum) -> List[ValidationMessage]:
        pass
