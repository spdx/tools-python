# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import pytest

from spdx_tools.spdx3.model import Hash, HashAlgorithm
from tests.spdx3.fixtures import hash_fixture
from tests.spdx3.model.model_test_utils import get_property_names


def test_correct_initialization():
    hash = hash_fixture()

    for property_name in get_property_names(Hash):
        assert getattr(hash, property_name) is not None

    assert hash.algorithm == HashAlgorithm.SHA1
    assert hash.hash_value == "71c4025dd9897b364f3ebbb42c484ff43d00791c"
    assert hash.comment == "hashComment"


def test_invalid_initialization():
    with pytest.raises(TypeError) as err:
        Hash("SHA1", 345)

    assert len(err.value.args[0]) == 2
    for error in err.value.args[0]:
        assert error.startswith("SetterError Hash:")
