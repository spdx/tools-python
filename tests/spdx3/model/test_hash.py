# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import pytest

from spdx_tools.spdx3.model import Hash, HashAlgorithm


def test_correct_initialization():
    hash = Hash(algorithm=HashAlgorithm.SHA1, hash_value="value")

    assert hash.algorithm == HashAlgorithm.SHA1
    assert hash.hash_value == "value"


def test_invalid_initialization():
    with pytest.raises(TypeError) as err:
        Hash("SHA1", 345)

    assert len(err.value.args[0]) == 2
    for error in err.value.args[0]:
        assert error.startswith("SetterError Hash:")
