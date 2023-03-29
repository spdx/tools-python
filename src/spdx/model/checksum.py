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
from enum import auto, Enum

from common.typing.dataclass_with_properties import dataclass_with_properties
from common.typing.type_checks import check_types_and_set_values


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
