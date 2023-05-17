# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from unittest import mock

import pytest

from spdx_tools.spdx3.model.software import Snippet, SoftwarePurpose


@mock.patch("spdx_tools.spdx3.model.software.Snippet", autospec=True)
def test_correct_initialization(creation_info):
    snippet = Snippet(
        "SPDXRef-Snippet",
        creation_info=creation_info,
        content_identifier="https://content.identifier",
        purpose=[SoftwarePurpose.SOURCE],
        byte_range=(3, 4),
        line_range=(346, 456),
    )

    assert snippet.spdx_id == "SPDXRef-Snippet"
    assert snippet.creation_info == creation_info
    assert snippet.content_identifier == "https://content.identifier"
    assert snippet.purpose == [SoftwarePurpose.SOURCE]
    assert snippet.byte_range == (3, 4)
    assert snippet.line_range == (346, 456)


@mock.patch("spdx_tools.spdx3.model.software.Snippet", autospec=True)
def test_invalid_initialization(creation_info):
    with pytest.raises(TypeError) as err:
        Snippet(2, creation_info=creation_info, originated_by=34, byte_range="34:45")

    assert len(err.value.args[0]) == 3
    for error in err.value.args[0]:
        assert error.startswith("SetterError Snippet:")
