# Copyright (c) 2014 Ahmed H. Ismail
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import re
from enum import Enum, auto



class ChecksumAlgorithmIdentifier(Enum):
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

    def checksum_to_rdf(self):
        return "checksumAlgorithm_" + self.name.lower()

    @classmethod
    def checksum_from_rdf(cls, identifier: str) -> str:
        identifier = identifier.split('_', 1)[-1].upper()
        blake_checksum = re.compile(r"(BLAKE2B)\s*(256|384|512)", re.UNICODE)
        match = blake_checksum.match(identifier)
        if match:
            return match[1] + '_' + match[2]
        return identifier


class Algorithm(object):
    """Generic checksum algorithm."""

    def __init__(self, identifier: str, value):
        if identifier.upper().replace('-', '_') not in ChecksumAlgorithmIdentifier.__members__:
            raise ValueError('Invalid algorithm for Checksum: {}'.format(identifier))
        self.identifier = identifier
        self.value = value

    def to_tv(self):
        return "{0}: {1}".format(self.identifier, self.value)
