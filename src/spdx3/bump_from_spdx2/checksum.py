#  Copyright (c) 2023 spdx contributors
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#    http://www.apache.org/licenses/LICENSE-2.0
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
from spdx.model.checksum import Checksum as Spdx2_Checksum, ChecksumAlgorithm
from spdx3.model.integrity_method import IntegrityMethod
from spdx3.model.hash import HashAlgorithm, Hash


def bump_checksum(spdx2_checksum: Spdx2_Checksum) -> IntegrityMethod:
    algorithm: HashAlgorithm = convert_checksum_algorithm_to_hash_algorithm(spdx2_checksum.algorithm)
    value: str = spdx2_checksum.value

    return Hash(algorithm, value)


def convert_checksum_algorithm_to_hash_algorithm(checksum_algorithm: ChecksumAlgorithm) -> HashAlgorithm:
    if checksum_algorithm.name.startswith("BLAKE"):
        return  HashAlgorithm[checksum_algorithm.name.replace("_","")]
    if checksum_algorithm == ChecksumAlgorithm.ADLER32:
        return HashAlgorithm.OTHER
    return HashAlgorithm[checksum_algorithm.name]
