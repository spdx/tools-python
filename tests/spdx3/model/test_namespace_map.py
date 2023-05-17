# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import pytest

from spdx_tools.spdx3.model import NamespaceMap
from tests.spdx3.fixtures import namespace_map_fixture
from tests.spdx3.model.model_test_utils import get_property_names


def test_correct_initialization():
    namespace_map = namespace_map_fixture()

    for property_name in get_property_names(NamespaceMap):
        assert getattr(namespace_map, property_name) is not None

    assert namespace_map.prefix == "namespaceMapPrefix"
    assert namespace_map.namespace == "https://spdx.test/tools-python/namespace_map_namespace"


def test_invalid_initialization():
    with pytest.raises(TypeError) as err:
        NamespaceMap(34, ["list of namespaces"])

    assert len(err.value.args[0]) == 2
    for error in err.value.args[0]:
        assert error.startswith("SetterError NamespaceMap:")
