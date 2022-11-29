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

    def algorithm_to_rdf_representation(self) -> str:
        if self.name.startswith("BLAKE2B"):
            return "checksumAlgorithm_" + self.name.replace("_", "").lower()
        else:
            return "checksumAlgorithm_" + self.name.lower()

    @classmethod
    def checksum_from_rdf(cls, identifier: str) -> 'ChecksumAlgorithm':
        identifier = identifier.split('_', 1)[-1].upper()
        blake_checksum = re.compile(r"^(BLAKE2B)(256|384|512)$", re.UNICODE)
        match = blake_checksum.match(identifier)
        if match:
            identifier = match[1] + '_' + match[2]
        if identifier not in ChecksumAlgorithm.__members__:
            raise ValueError(f"Invalid algorithm for checksum: {identifier}")
        return ChecksumAlgorithm[identifier]

    @classmethod
    def checksum_algorithm_from_string(cls, identifier: str) -> 'ChecksumAlgorithm':
        identifier = identifier.replace("-", "_").upper()
        if identifier not in ChecksumAlgorithm.__members__:
            raise ValueError(f"Invalid algorithm for checksum: {identifier}")
        return ChecksumAlgorithm[identifier]


class Checksum(object):
    """Generic checksum algorithm."""

    def __init__(self, identifier: ChecksumAlgorithm, value: str):
        self.identifier = identifier
        self.value = value

    def __eq__(self, other) -> bool:
        if not isinstance(other, Checksum):
            return False
        return self.identifier == other.identifier and self.value == other.value

    @classmethod
    def checksum_from_string(cls, value: str) -> 'Checksum':
        CHECKSUM_RE = re.compile("(ADLER32|BLAKE2b-256|BLAKE2b-384|BLAKE2b-512|BLAKE3|MD2|MD4|MD5|MD6|" \
                                 "SHA1|SHA224|SHA256|SHA384|SHA512|SHA3-256|SHA3-384|SHA3-512):\\s*([a-fA-F0-9]*)")
        match = CHECKSUM_RE.match(value)
        if match is None or match.group(1) is None or match.group(2) is None:
            raise ValueError(f"Invalid checksum: {value}")
        identifier = ChecksumAlgorithm.checksum_algorithm_from_string(match.group(1))
        return Checksum(identifier=identifier, value=match.group(2))

    def to_tv(self) -> str:
        algorithm_name: str = self.identifier.name
        # Convert underscores to dashes, and other Blake2b-specific casing rules
        if "_" in algorithm_name:
            algorithm_name = CHECKSUM_ALGORITHM_TO_TV.get(algorithm_name)
            if algorithm_name is None:
                raise ValueError(f"Missing conversion rule for converting {self.identifier.name} to tag-value string")
        return "{0}: {1}".format(algorithm_name, self.value)


CHECKSUM_ALGORITHM_TO_TV = {
    ChecksumAlgorithm.BLAKE2B_256.name: "BLAKE2b-256",
    ChecksumAlgorithm.BLAKE2B_384.name: "BLAKE2b-384",
    ChecksumAlgorithm.BLAKE2B_512.name: "BLAKE2b-512",
    ChecksumAlgorithm.SHA3_256.name: "SHA3-256",
    ChecksumAlgorithm.SHA3_384.name: "SHA3-384",
    ChecksumAlgorithm.SHA3_512.name: "SHA3-512"
}
