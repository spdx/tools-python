import re
from typing import List, Dict

from src.model.checksum import Checksum, ChecksumAlgorithm
from src.validation.validation_message import ValidationMessage, ValidationContext, SpdxElementType

# in hexadecimal digits
algorithm_length: Dict = {
    ChecksumAlgorithm.SHA1: "40",
    ChecksumAlgorithm.SHA224: "56",
    ChecksumAlgorithm.SHA256: "64",
    ChecksumAlgorithm.SHA384: "96",
    ChecksumAlgorithm.SHA512: "128",
    ChecksumAlgorithm.SHA3_256: "64",
    ChecksumAlgorithm.SHA3_384: "96",
    ChecksumAlgorithm.SHA3_512: "128",
    ChecksumAlgorithm.BLAKE2B_256: "64",
    ChecksumAlgorithm.BLAKE2B_384: "96",
    ChecksumAlgorithm.BLAKE2B_512: "128",
    ChecksumAlgorithm.BLAKE3: "256,",  # at least 256 bits
    ChecksumAlgorithm.MD2: "32",
    ChecksumAlgorithm.MD4: "32",
    ChecksumAlgorithm.MD5: "32",
    ChecksumAlgorithm.MD6: "0,512",  # between 0 and 512 bits
    ChecksumAlgorithm.ADLER32: "8",
}


class ChecksumValidator:
    spdx_version: str
    parent_id: str

    def __init__(self, spdx_version: str, parent_id: str):
        self.spdx_version = spdx_version
        self.parent_id = parent_id

    def validate_checksums(self, checksums: List[Checksum]) -> List[ValidationMessage]:
        validation_messages = []
        for checksum in checksums:
            validation_messages.extend(self.validate_checksum(checksum))

        return validation_messages

    def validate_checksum(self, checksum: Checksum) -> List[ValidationMessage]:
        validation_messages = []
        algorithm = checksum.algorithm
        context = ValidationContext(parent_id=self.parent_id, element_type=SpdxElementType.CHECKSUM, full_element=checksum)

        if not re.match("^[0-9a-f]{" + algorithm_length[algorithm] + "}$", checksum.value):
            if algorithm == ChecksumAlgorithm.BLAKE3:
                length = "at least 256"
            elif algorithm == ChecksumAlgorithm.MD6:
                length = "between 0 and 512"
            else:
                length = algorithm_length[algorithm]
            validation_messages.append(
                ValidationMessage(f'value of {algorithm} must consist of {length} hexadecimal digits, but is: {checksum.value} (length: {len(checksum.value)} digits)', context)
            )

        return validation_messages
