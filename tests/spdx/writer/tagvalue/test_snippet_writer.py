# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from unittest.mock import MagicMock, call, mock_open, patch

from spdx_tools.spdx.writer.tagvalue.snippet_writer import write_snippet
from tests.spdx.fixtures import snippet_fixture


def test_snippet_writer():
    snippet = snippet_fixture()

    mock: MagicMock = mock_open()
    with patch(f"{__name__}.open", mock, create=True):
        with open("foo", "w") as file:
            write_snippet(snippet, file)

    mock.assert_called_once_with("foo", "w")
    handle = mock()
    handle.write.assert_has_calls(
        [
            call("## Snippet Information\n"),
            call(f"SnippetSPDXID: {snippet.spdx_id}\n"),
            call(f"SnippetFromFileSPDXID: {snippet.file_spdx_id}\n"),
            call("SnippetByteRange: 1:2\n"),
            call("SnippetLineRange: 3:4\n"),
            call(f"SnippetLicenseConcluded: {snippet.license_concluded}\n"),
            call(f"LicenseInfoInSnippet: {snippet.license_info_in_snippet[0]}\n"),
            call(f"LicenseInfoInSnippet: {snippet.license_info_in_snippet[1]}\n"),
            call(f"LicenseInfoInSnippet: {snippet.license_info_in_snippet[2]}\n"),
            call(f"SnippetLicenseComments: {snippet.license_comment}\n"),
            call(f"SnippetCopyrightText: {snippet.copyright_text}\n"),
            call(f"SnippetComment: {snippet.comment}\n"),
            call(f"SnippetName: {snippet.name}\n"),
            call(f"SnippetAttributionText: {snippet.attribution_texts[0]}\n"),
        ]
    )
