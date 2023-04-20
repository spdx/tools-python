# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from unittest import mock

import pytest

from spdx_tools.spdx3.model import Bundle


@mock.patch("spdx_tools.spdx3.model.NamespaceMap", autospec=True)
@mock.patch("spdx_tools.spdx3.model.CreationInformation", autospec=True)
def test_correct_initialization(creation_information, namespace):
    bundle = Bundle(
        "SPDXRef-Bundle",
        creation_information,
        elements=["spdx_id1"],
        root_elements=["spdx_id2"],
        namespaces=[namespace],
        context="context",
    )

    assert bundle.spdx_id == "SPDXRef-Bundle"
    assert bundle.creation_info == creation_information
    assert bundle.elements == ["spdx_id1"]
    assert bundle.root_elements == ["spdx_id2"]
    assert bundle.context == "context"
    assert bundle.namespaces == [namespace]


@mock.patch("spdx_tools.spdx3.model.CreationInformation", autospec=True)
def test_invalid_initialization(creation_information):
    with pytest.raises(TypeError) as err:
        Bundle(4, creation_information, elements="spdx_id1", root_elements=[42], namespaces=True, context=["yes"])

    assert err.value.args[0] == [
        'SetterError Bundle: type of argument "spdx_id" must be str; got int instead: 4',
        'SetterError Bundle: type of argument "elements" must be a list; got str ' "instead: spdx_id1",
        'SetterError Bundle: type of argument "root_elements"[0] must be str; got int ' "instead: [42]",
        'SetterError Bundle: type of argument "namespaces" must be a list; ' "got bool instead: True",
        'SetterError Bundle: type of argument "context" must be one of (str, ' "NoneType); got list instead: ['yes']",
    ]
