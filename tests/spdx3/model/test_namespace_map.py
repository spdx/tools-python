# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import pytest

from spdx_tools.spdx3.model import NamespaceMap


def test_correct_initialization():
    namespace_map = NamespaceMap("some prefix", "https://namespace")

    assert namespace_map.prefix == "some prefix"
    assert namespace_map.namespace == "https://namespace"


def test_invalid_initialization():
    with pytest.raises(TypeError) as err:
        NamespaceMap(34, ["list of namespaces"])

    assert err.value.args[0] == [
        'SetterError NamespaceMap: type of argument "prefix" must be one of (str, ' "NoneType); got int instead: 34",
        'SetterError NamespaceMap: type of argument "namespace" must be one of (str, '
        "NoneType); got list instead: ['list of namespaces']",
    ]
