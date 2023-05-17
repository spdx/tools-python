# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from unittest import mock

import pytest

from spdx_tools.spdx3.model.software import File, SoftwarePurpose


@mock.patch("spdx_tools.spdx3.model.CreationInfo", autospec=True)
def test_correct_initialization(creation_info):
    file = File(
        "SPDXRef-File",
        "Test file",
        creation_info=creation_info,
        verified_using=None,
        content_identifier="https://any.uri",
        purpose=[SoftwarePurpose.ARCHIVE, SoftwarePurpose.FILE],
        content_type="MediaType",
    )

    assert file.spdx_id == "SPDXRef-File"
    assert file.creation_info == creation_info
    assert file.name == "Test file"
    assert file.content_identifier == "https://any.uri"
    assert file.purpose == [SoftwarePurpose.ARCHIVE, SoftwarePurpose.FILE]
    assert file.content_type == "MediaType"


@mock.patch("spdx_tools.spdx3.model.CreationInfo", autospec=True)
def test_invalid_initialization(creation_info):
    with pytest.raises(TypeError) as err:
        File(
            1,
            "test file",
            creation_info=creation_info,
            content_identifier=3,
            purpose=SoftwarePurpose.FILE,
            content_type=SoftwarePurpose.ARCHIVE,
        )

    assert len(err.value.args[0]) == 4
    for error in err.value.args[0]:
        assert error.startswith("SetterError File:")
