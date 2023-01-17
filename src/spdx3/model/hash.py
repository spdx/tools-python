# Copyright (c) 2023 spdx contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#    http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from enum import Enum, auto
from typing import Optional

from common.typing.dataclass_with_properties import dataclass_with_properties
from common.typing.type_checks import check_types_and_set_values
from spdx3.model.integrity_method import IntegrityMethod

class HashAlgorithm(Enum):
    BLAKE2B256 = auto()
    BLAKE2B384 = auto()
    BLAKE2B512 = auto()
    BLAKE3 = auto()
    MD2 = auto()
    MD4 = auto()
    MD5 = auto()
    MD6 = auto()
    OTHER = auto()
    SHA1 = auto()
    SHA224 = auto()
    SHA256 = auto()
    SHA3_224 = auto()
    SHA3_256 = auto()
    SHA3_384 = auto()
    SHA3_512 = auto()
    SHA384 = auto()
    SHA512 = auto()
    SPDXPVCSHA1 = auto()
    SPDXPVCSHA256 = auto()


@dataclass_with_properties
class Hash(IntegrityMethod):
    algorithm: HashAlgorithm = None
    hash_value: str = None
    # We overwrite the super-__init__ as check_types_and_set_values() takes care of all fields (including inherited ones).

    def __init__(self, algorithm: HashAlgorithm, hash_value: str, comment: Optional[str] = None):
        check_types_and_set_values(self, locals())

