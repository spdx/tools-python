import pytest

from spdx.model.checksum import Checksum, ChecksumAlgorithm


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
