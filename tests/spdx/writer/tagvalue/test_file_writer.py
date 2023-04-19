# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from unittest.mock import MagicMock, call, mock_open, patch

from spdx_tools.spdx.writer.tagvalue.file_writer import write_file
from tests.spdx.fixtures import file_fixture


def test_file_writer():
    spdx_file = file_fixture()

    mock: MagicMock = mock_open()
    with patch(f"{__name__}.open", mock, create=True):
        with open("foo", "w") as file:
            write_file(spdx_file, file)

    mock.assert_called_once_with("foo", "w")
    handle = mock()
    handle.write.assert_has_calls(
        [
            call("## File Information\n"),
            call(f"FileName: {spdx_file.name}\n"),
            call(f"SPDXID: {spdx_file.spdx_id}\n"),
            call(f"FileType: {spdx_file.file_types[0].name}\n"),
            call("FileChecksum: SHA1: 71c4025dd9897b364f3ebbb42c484ff43d00791c\n"),
            call(f"LicenseConcluded: {spdx_file.license_concluded}\n"),
            call(f"LicenseInfoInFile: {spdx_file.license_info_in_file[0]}\n"),
            call(f"LicenseInfoInFile: {spdx_file.license_info_in_file[1]}\n"),
            call(f"LicenseInfoInFile: {spdx_file.license_info_in_file[2]}\n"),
            call(f"LicenseComments: {spdx_file.license_comment}\n"),
            call(f"FileCopyrightText: {spdx_file.copyright_text}\n"),
            call(f"FileComment: {spdx_file.comment}\n"),
            call(f"FileNotice: {spdx_file.notice}\n"),
            call(f"FileContributor: {spdx_file.contributors[0]}\n"),
            call(f"FileAttributionText: {spdx_file.attribution_texts[0]}\n"),
        ]
    )
