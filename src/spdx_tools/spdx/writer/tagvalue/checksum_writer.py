# SPDX-License-Identifier: Apache-2.0
#  Copyright (c) 2022 spdx contributors
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#    http://www.apache.org/licenses/LICENSE-2.0
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
from spdx_tools.spdx.model import Checksum, ChecksumAlgorithm


def write_checksum_to_tag_value(checksum: Checksum) -> str:
    algorithm_name: str = checksum.algorithm.name
    # Convert underscores to dashes, and other Blake2b-specific casing rules
    if "_" in algorithm_name:
        algorithm_name = CHECKSUM_ALGORITHM_TO_TV.get(algorithm_name)
        if algorithm_name is None:
            raise ValueError(f"Missing conversion rule for converting {checksum.algorithm.name} to tag-value string")
    return f"{algorithm_name}: {checksum.value}"


CHECKSUM_ALGORITHM_TO_TV = {
    ChecksumAlgorithm.BLAKE2B_256.name: "BLAKE2b-256",
    ChecksumAlgorithm.BLAKE2B_384.name: "BLAKE2b-384",
    ChecksumAlgorithm.BLAKE2B_512.name: "BLAKE2b-512",
    ChecksumAlgorithm.SHA3_256.name: "SHA3-256",
    ChecksumAlgorithm.SHA3_384.name: "SHA3-384",
    ChecksumAlgorithm.SHA3_512.name: "SHA3-512",
}
