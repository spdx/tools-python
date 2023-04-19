# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from unittest.mock import MagicMock, call, mock_open, patch

from spdx_tools.spdx.writer.tagvalue.extracted_licensing_info_writer import write_extracted_licensing_info
from tests.spdx.fixtures import extracted_licensing_info_fixture


def test_extracted_licensing_info_writer():
    extracted_licensing_info = extracted_licensing_info_fixture()

    mock: MagicMock = mock_open()
    with patch(f"{__name__}.open", mock, create=True):
        with open("foo", "w") as file:
            write_extracted_licensing_info(extracted_licensing_info, file)

    mock.assert_called_once_with("foo", "w")
    handle = mock()
    handle.write.assert_has_calls(
        [
            call(f"LicenseID: {extracted_licensing_info.license_id}\n"),
            call(f"ExtractedText: {extracted_licensing_info.extracted_text}\n"),
            call(f"LicenseName: {extracted_licensing_info.license_name}\n"),
            call(f"LicenseCrossReference: {extracted_licensing_info.cross_references[0]}\n"),
            call(f"LicenseComment: {extracted_licensing_info.comment}\n"),
        ]
    )
