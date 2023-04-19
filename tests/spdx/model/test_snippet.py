# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0

import pytest

from spdx_tools.spdx.model import Snippet, SpdxNoAssertion, SpdxNone


def test_correct_initialization():
    snippet = Snippet(
        "id",
        "file_id",
        (200, 400),
        (20, 40),
        SpdxNone(),
        [SpdxNoAssertion()],
        "comment on license",
        "copyright",
        "comment",
        "name",
        ["attribution"],
    )
    assert snippet.spdx_id == "id"
    assert snippet.file_spdx_id == "file_id"
    assert snippet.byte_range == (200, 400)
    assert snippet.line_range == (20, 40)
    assert snippet.license_concluded == SpdxNone()
    assert snippet.license_info_in_snippet == [SpdxNoAssertion()]
    assert snippet.license_comment == "comment on license"
    assert snippet.copyright_text == "copyright"
    assert snippet.comment == "comment"
    assert snippet.name == "name"
    assert snippet.attribution_texts == ["attribution"]


def test_correct_initialization_with_default_values():
    snippet = Snippet("id", "file_id", (200, 400))
    assert snippet.spdx_id == "id"
    assert snippet.file_spdx_id == "file_id"
    assert snippet.byte_range == (200, 400)
    assert snippet.line_range is None
    assert snippet.license_concluded is None
    assert snippet.license_info_in_snippet == []
    assert snippet.license_comment is None
    assert snippet.copyright_text is None
    assert snippet.comment is None
    assert snippet.name is None
    assert snippet.attribution_texts == []


def test_wrong_type_in_spdx_id():
    with pytest.raises(TypeError):
        Snippet(42, "file_id", (200, 400))


def test_wrong_type_in_file_spdx_id():
    with pytest.raises(TypeError):
        Snippet("id", 42, (200, 400))


def test_wrong_type_in_byte_range():
    with pytest.raises(TypeError):
        Snippet("id", "file_id", (200, 300, 400))


def test_wrong_type_in_line_range():
    with pytest.raises(TypeError):
        Snippet("id", "file_id", (200, 400), line_range=(20, "40"))


def test_wrong_type_in_license_concluded():
    with pytest.raises(TypeError):
        Snippet("id", "file_id", (200, 400), license_concluded="NONE")


def test_wrong_type_in_license_info_in_snippet():
    with pytest.raises(TypeError):
        Snippet("id", "file_id", (200, 400), license_info_in_snippet=SpdxNoAssertion())


def test_wrong_type_in_license_comment():
    with pytest.raises(TypeError):
        Snippet("id", "file_id", (200, 400), license_comment=[])


def test_wrong_type_in_copyright_text():
    with pytest.raises(TypeError):
        Snippet("id", "file_id", (200, 400), copyright_text=["copyright"])


def test_wrong_type_in_comment():
    with pytest.raises(TypeError):
        Snippet("id", "file_id", (200, 400), comment=["comment"])


def test_wrong_type_in_name():
    with pytest.raises(TypeError):
        Snippet("id", "file_id", (200, 400), name=42)


def test_wrong_type_in_attribution_texts():
    with pytest.raises(TypeError):
        Snippet("id", "file_id", (200, 400), attribution_texts="attribution")
