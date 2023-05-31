# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0

from unittest import mock

from spdx_tools.spdx.model import File, FileType, SpdxNoAssertion, SpdxNone


@mock.patch("spdx_tools.spdx.model.Checksum", autospec=True)
def test_correct_initialization(checksum):
    file = File(
        "name",
        "id",
        [checksum, checksum],
        [FileType.OTHER, FileType.SPDX],
        SpdxNone(),
        [SpdxNoAssertion()],
        "comment on license",
        "copyright",
        "comment",
        "notice",
        ["contributor"],
        ["attribution"],
    )
    assert file.name == "name"
    assert file.spdx_id == "id"
    assert file.checksums == [checksum, checksum]
    assert file.file_types == [FileType.OTHER, FileType.SPDX]
    assert file.license_concluded == SpdxNone()
    assert file.license_info_in_file == [SpdxNoAssertion()]
    assert file.license_comment == "comment on license"
    assert file.copyright_text == "copyright"
    assert file.comment == "comment"
    assert file.notice == "notice"
    assert file.contributors == ["contributor"]
    assert file.attribution_texts == ["attribution"]


@mock.patch("spdx_tools.spdx.model.Checksum", autospec=True)
def test_correct_initialization_with_default_values(checksum):
    file = File("name", "id", [checksum, checksum])
    assert file.name == "name"
    assert file.spdx_id == "id"
    assert file.checksums == [checksum, checksum]
    assert file.file_types == []
    assert file.license_concluded is None
    assert file.license_info_in_file == []
    assert file.license_comment is None
    assert file.copyright_text is None
    assert file.comment is None
    assert file.notice is None
    assert file.contributors == []
    assert file.attribution_texts == []
