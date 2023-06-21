# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0

import pytest

from spdx_tools.spdx3.model import ExternalMap
from tests.spdx3.fixtures import external_map_fixture, hash_fixture
from tests.spdx3.model.model_test_utils import get_property_names


def test_correct_initialization():
    external_map = external_map_fixture()

    for property_name in get_property_names(ExternalMap):
        assert getattr(external_map, property_name) is not None

    assert external_map.external_id == "https://spdx.test/tools-python/external_map_external_id"
    assert external_map.verified_using == [hash_fixture()]
    assert external_map.location_hint == "https://spdx.test/tools-python/external_map_location_hint"
    assert external_map.defining_document == "https://spdx.test/tools-python/defining_document"


def test_invalid_initialization():
    with pytest.raises(TypeError) as err:
        ExternalMap(234, None, ["location  hints"])

    assert len(err.value.args[0]) == 2
    for error in err.value.args[0]:
        assert error.startswith("SetterError ExternalMap:")
