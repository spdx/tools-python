# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from spdx_tools.spdx3.model import Hash, HashAlgorithm
from spdx_tools.spdx.model.checksum import Checksum as Spdx2_Checksum
from spdx_tools.spdx.model.checksum import ChecksumAlgorithm


def bump_checksum(spdx2_checksum: Spdx2_Checksum) -> Hash:
    algorithm: HashAlgorithm = convert_checksum_algorithm_to_hash_algorithm(spdx2_checksum.algorithm)
    value: str = spdx2_checksum.value

    return Hash(algorithm, value)


def convert_checksum_algorithm_to_hash_algorithm(checksum_algorithm: ChecksumAlgorithm) -> HashAlgorithm:
    if checksum_algorithm.name.startswith("BLAKE"):
        return HashAlgorithm[checksum_algorithm.name.replace("_", "")]
    if checksum_algorithm == ChecksumAlgorithm.ADLER32:
        return HashAlgorithm.OTHER
    return HashAlgorithm[checksum_algorithm.name]
