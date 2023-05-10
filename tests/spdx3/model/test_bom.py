# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0

from unittest import mock

import pytest

from spdx_tools.spdx3.model import Bom


@mock.patch("spdx_tools.spdx3.model.CreationInformation", autospec=True)
def test_correct_initialization(creation_information):
    bom = Bom("SPDXRef-Bom", creation_information, element=["spdx_id1"], root_element=["spdx_id2"])

    assert bom.spdx_id == "SPDXRef-Bom"
    assert bom.creation_info == creation_information
    assert bom.element == ["spdx_id1"]
    assert bom.root_element == ["spdx_id2"]


def test_invalid_initialization():
    with pytest.raises(TypeError) as err:
        Bom(1, "Creation Information", element=[5], root_element=[])

    assert err.value.args[0] == [
        'SetterError Bom: type of argument "spdx_id" must be str; got int instead: 1',
        'SetterError Bom: type of argument "creation_info" must be '
        "spdx_tools.spdx3.model.creation_information.CreationInformation; got str "
        "instead: Creation Information",
        'SetterError Bom: type of argument "element"[0] must be str; got int instead: ' "[5]",
    ]
