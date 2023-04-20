# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from unittest import mock

import pytest

from spdx_tools.spdx3.model.software import Snippet, SoftwarePurpose


@mock.patch("spdx_tools.spdx3.model.software.Snippet", autospec=True)
def test_correct_initialization(creation_information):
    snippet = Snippet(
        "SPDXRef-Snippet",
        creation_information,
        content_identifier="https://content.identifier",
        snippet_purpose=[SoftwarePurpose.SOURCE],
        byte_range=(3, 4),
        line_range=(346, 456),
    )

    assert snippet.spdx_id == "SPDXRef-Snippet"
    assert snippet.creation_info == creation_information
    assert snippet.content_identifier == "https://content.identifier"
    assert snippet.snippet_purpose == [SoftwarePurpose.SOURCE]
    assert snippet.byte_range == (3, 4)
    assert snippet.line_range == (346, 456)


@mock.patch("spdx_tools.spdx3.model.software.Snippet", autospec=True)
def test_invalid_initialization(creation_information):
    with pytest.raises(TypeError) as err:
        Snippet(2, creation_information, originated_by=34, byte_range="34:45")

    assert err.value.args[0] == [
        'SetterError Snippet: type of argument "spdx_id" must be str; got int ' "instead: 2",
        'SetterError Snippet: type of argument "originated_by" must be one of (str, ' "NoneType); got int instead: 34",
        'SetterError Snippet: type of argument "byte_range" must be one of '
        "(Tuple[int, int], NoneType); got str instead: 34:45",
    ]
