# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import pytest

from spdx_tools.spdx.model import ChecksumAlgorithm
from spdx_tools.spdx.writer.tagvalue.checksum_writer import write_checksum_to_tag_value
from tests.spdx.fixtures import checksum_fixture


@pytest.mark.parametrize(
    "checksum, expected_string",
    [
        (checksum_fixture(), "SHA1: 71c4025dd9897b364f3ebbb42c484ff43d00791c"),
        (checksum_fixture(algorithm=ChecksumAlgorithm.SHA3_256, value="fdsef"), "SHA3-256: fdsef"),
        (checksum_fixture(algorithm=ChecksumAlgorithm.SHA3_384, value="fdsef"), "SHA3-384: fdsef"),
        (checksum_fixture(algorithm=ChecksumAlgorithm.SHA3_512, value="fdsef"), "SHA3-512: fdsef"),
        (checksum_fixture(algorithm=ChecksumAlgorithm.BLAKE2B_256, value="fdsef"), "BLAKE2b-256: fdsef"),
        (checksum_fixture(algorithm=ChecksumAlgorithm.BLAKE2B_384, value="fdsef"), "BLAKE2b-384: fdsef"),
        (checksum_fixture(algorithm=ChecksumAlgorithm.BLAKE2B_512, value="fdsef"), "BLAKE2b-512: fdsef"),
    ],
)
def test_checksum_writer(checksum, expected_string):
    checksum_string = write_checksum_to_tag_value(checksum)

    assert checksum_string == expected_string
