# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0

from spdx_tools.spdx.model import Checksum, ChecksumAlgorithm


def test_correct_initialization():
    checksum = Checksum(ChecksumAlgorithm.BLAKE2B_256, "value")
    assert checksum.algorithm == ChecksumAlgorithm.BLAKE2B_256
    assert checksum.value == "value"
