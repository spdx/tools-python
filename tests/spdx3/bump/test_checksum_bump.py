# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import pytest

from spdx_tools.spdx3.bump_from_spdx2.checksum import bump_checksum, convert_checksum_algorithm_to_hash_algorithm
from spdx_tools.spdx3.model import HashAlgorithm
from spdx_tools.spdx.model.checksum import ChecksumAlgorithm
from tests.spdx.fixtures import checksum_fixture


def test_bump_checksum():
    checksum = checksum_fixture()
    hash = bump_checksum(checksum)

    assert hash.algorithm == HashAlgorithm.SHA1
    assert hash.hash_value == "71c4025dd9897b364f3ebbb42c484ff43d00791c"


@pytest.mark.parametrize(
    "checksum_algorithm,expected_hash_algorithm",
    [
        (ChecksumAlgorithm.SHA1, HashAlgorithm.SHA1),
        (ChecksumAlgorithm.SHA224, HashAlgorithm.SHA224),
        (ChecksumAlgorithm.SHA256, HashAlgorithm.SHA256),
        (ChecksumAlgorithm.SHA384, HashAlgorithm.SHA384),
        (ChecksumAlgorithm.SHA512, HashAlgorithm.SHA512),
        (ChecksumAlgorithm.SHA3_256, HashAlgorithm.SHA3_256),
        (ChecksumAlgorithm.SHA3_384, HashAlgorithm.SHA3_384),
        (ChecksumAlgorithm.SHA3_512, HashAlgorithm.SHA3_512),
        (ChecksumAlgorithm.BLAKE2B_256, HashAlgorithm.BLAKE2B256),
        (ChecksumAlgorithm.BLAKE2B_384, HashAlgorithm.BLAKE2B384),
        (ChecksumAlgorithm.BLAKE2B_512, HashAlgorithm.BLAKE2B512),
        (ChecksumAlgorithm.BLAKE3, HashAlgorithm.BLAKE3),
        (ChecksumAlgorithm.MD2, HashAlgorithm.MD2),
        (ChecksumAlgorithm.MD4, HashAlgorithm.MD4),
        (ChecksumAlgorithm.MD5, HashAlgorithm.MD5),
        (ChecksumAlgorithm.MD6, HashAlgorithm.MD6),
        (ChecksumAlgorithm.ADLER32, HashAlgorithm.OTHER),
    ],
)
def test_bump_checksum_algorithm(checksum_algorithm, expected_hash_algorithm):
    hash_algorithm = convert_checksum_algorithm_to_hash_algorithm(checksum_algorithm)

    assert hash_algorithm == expected_hash_algorithm
