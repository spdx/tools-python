# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0

from unittest import mock

import pytest

from spdx_tools.spdx.model import Checksum, ChecksumAlgorithm, File, FileType, SpdxNoAssertion, SpdxNone


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


@mock.patch("spdx_tools.spdx.model.Checksum", autospec=True)
def test_wrong_type_in_name(checksum):
    with pytest.raises(TypeError):
        File(42, "id", [checksum])


@mock.patch("spdx_tools.spdx.model.Checksum", autospec=True)
def test_wrong_type_in_spdx_id(checksum):
    with pytest.raises(TypeError):
        File("name", 42, [checksum])


def test_wrong_type_in_checksum():
    checksum = Checksum(ChecksumAlgorithm.BLAKE2B_256, "value")
    with pytest.raises(TypeError):
        File("name", "id", checksum)


@mock.patch("spdx_tools.spdx.model.Checksum", autospec=True)
def test_wrong_type_in_file_type(checksum):
    with pytest.raises(TypeError):
        File("name", "id", [checksum], file_types=FileType.OTHER)


@mock.patch("spdx_tools.spdx.model.Checksum", autospec=True)
def test_wrong_type_in_license_concluded(checksum):
    with pytest.raises(TypeError):
        File("name", "id", [checksum], license_concluded="NONE")


@mock.patch("spdx_tools.spdx.model.Checksum", autospec=True)
def test_wrong_type_in_license_info_in_file(checksum):
    with pytest.raises(TypeError):
        File("name", "id", [checksum], license_info_in_file=[SpdxNone])


@mock.patch("spdx_tools.spdx.model.Checksum", autospec=True)
def test_wrong_type_in_license_comment(checksum):
    with pytest.raises(TypeError):
        File("name", "id", [checksum], license_comment=42)


@mock.patch("spdx_tools.spdx.model.Checksum", autospec=True)
def test_wrong_type_in_copyright_text(checksum):
    with pytest.raises(TypeError):
        File("name", "id", [checksum], copyright_text=[SpdxNone()])


@mock.patch("spdx_tools.spdx.model.Checksum", autospec=True)
def test_wrong_type_in_comment(checksum):
    with pytest.raises(TypeError):
        File("name", "id", [checksum], comment=42)


@mock.patch("spdx_tools.spdx.model.Checksum", autospec=True)
def test_wrong_type_in_notice(checksum):
    with pytest.raises(TypeError):
        File("name", "id", [checksum], notice=["notice"])


@mock.patch("spdx_tools.spdx.model.Checksum", autospec=True)
def test_wrong_type_in_contributors(checksum):
    with pytest.raises(TypeError):
        File("name", "id", [checksum], contributors="contributor")


@mock.patch("spdx_tools.spdx.model.Checksum", autospec=True)
def test_wrong_type_in_attribution_texts(checksum):
    with pytest.raises(TypeError):
        File("name", "id", [checksum], attribution_texts=[41, 42])
