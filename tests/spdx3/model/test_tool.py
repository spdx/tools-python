# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from datetime import datetime

import pytest
from semantic_version import Version

from spdx_tools.spdx3.model.creation_information import CreationInformation
from spdx_tools.spdx3.model.tool import Tool


def test_correct_initialization():
    agent = Tool(
        "SPDXRef-Tool",
        CreationInformation(Version("3.0.0"), datetime(2023, 1, 1), ["SPDXRef-Agent"], [], ["core"], "CC0"),
    )

    assert agent.spdx_id == "SPDXRef-Tool"
    assert agent.creation_info == CreationInformation(
        Version("3.0.0"), datetime(2023, 1, 1), ["SPDXRef-Agent"], [], ["core"], "CC0"
    )


def test_invalid_initialization():
    with pytest.raises(TypeError) as err:
        Tool(12, 345)

    assert err.value.args[0] == [
        'SetterError Tool: type of argument "spdx_id" must be str; got int instead: 12',
        'SetterError Tool: type of argument "creation_info" must be '
        "spdx_tools.spdx3.model.creation_information.CreationInformation; got int instead: 345",
    ]
