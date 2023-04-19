# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from enum import Enum, auto

from spdx_tools.common.typing.dataclass_with_properties import dataclass_with_properties
from spdx_tools.common.typing.type_checks import check_types_and_set_values


class ChecksumAlgorithm(Enum):
    SHA1 = auto()
    SHA224 = auto()
    SHA256 = auto()
    SHA384 = auto()
    SHA512 = auto()
    SHA3_256 = auto()
    SHA3_384 = auto()
    SHA3_512 = auto()
    BLAKE2B_256 = auto()
    BLAKE2B_384 = auto()
    BLAKE2B_512 = auto()
    BLAKE3 = auto()
    MD2 = auto()
    MD4 = auto()
    MD5 = auto()
    MD6 = auto()
    ADLER32 = auto()


@dataclass_with_properties
class Checksum:
    algorithm: ChecksumAlgorithm
    value: str

    def __init__(self, algorithm: ChecksumAlgorithm, value: str):
        check_types_and_set_values(self, locals())
