# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0

import re

from beartype.typing import Dict, List

from spdx_tools.spdx.model import Checksum, ChecksumAlgorithm
from spdx_tools.spdx.validation.validation_message import SpdxElementType, ValidationContext, ValidationMessage

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


def validate_checksums(checksums: List[Checksum], parent_id: str, spdx_version: str) -> List[ValidationMessage]:
    validation_messages = []
    for checksum in checksums:
        validation_messages.extend(validate_checksum(checksum, parent_id, spdx_version))

    return validation_messages


def validate_checksum(checksum: Checksum, parent_id: str, spdx_version: str) -> List[ValidationMessage]:
    validation_messages = []
    algorithm = checksum.algorithm
    context = ValidationContext(parent_id=parent_id, element_type=SpdxElementType.CHECKSUM, full_element=checksum)

    if spdx_version == "SPDX-2.2" and algorithm in [
        ChecksumAlgorithm.SHA3_512,
        ChecksumAlgorithm.SHA3_384,
        ChecksumAlgorithm.SHA3_256,
        ChecksumAlgorithm.BLAKE3,
        ChecksumAlgorithm.BLAKE2B_512,
        ChecksumAlgorithm.BLAKE2B_384,
        ChecksumAlgorithm.BLAKE2B_256,
        ChecksumAlgorithm.ADLER32,
    ]:
        return [ValidationMessage(f"{checksum.algorithm.name} is not supported in SPDX-2.2", context)]

    if not re.match("^[0-9a-f]{" + algorithm_length[algorithm] + "}$", checksum.value):
        if algorithm == ChecksumAlgorithm.BLAKE3:
            length = "at least 256"
        elif algorithm == ChecksumAlgorithm.MD6:
            length = "between 0 and 512"
        else:
            length = algorithm_length[algorithm]
        validation_messages.append(
            ValidationMessage(
                f"value of {algorithm} must consist of {length} lowercase hexadecimal digits, but is: "
                f"{checksum.value} (length: {len(checksum.value)} digits)",
                context,
            )
        )

    return validation_messages
