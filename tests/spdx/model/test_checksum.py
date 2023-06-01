# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0

import pytest

from spdx_tools.spdx.model import Checksum, ChecksumAlgorithm


def test_correct_initialization():
    checksum = Checksum(ChecksumAlgorithm.BLAKE2B_256, "value")
    assert checksum.algorithm == ChecksumAlgorithm.BLAKE2B_256
    assert checksum.value == "value"


def test_wrong_type_in_algorithm():
    with pytest.raises(TypeError):
        Checksum(42, "value")


def test_wrong_type_in_value():
    with pytest.raises(TypeError):
        Checksum(ChecksumAlgorithm.BLAKE2B_256, 42)
