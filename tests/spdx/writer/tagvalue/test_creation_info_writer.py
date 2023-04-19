# SPDX-FileCopyrightText: 2023 SPDX Contributors
#
# SPDX-License-Identifier: Apache-2.0
import datetime
from unittest.mock import MagicMock, call, mock_open, patch

import pytest

from spdx_tools.spdx.constants import DOCUMENT_SPDX_ID
from spdx_tools.spdx.model import CreationInfo
from spdx_tools.spdx.writer.tagvalue.creation_info_writer import write_creation_info
from tests.spdx.fixtures import actor_fixture, creation_info_fixture


@pytest.mark.parametrize(
    "creation_info, expected_calls",
    [
        (
            creation_info_fixture(),
            [
                call("SPDXVersion: SPDX-2.3\n"),
                call("DataLicense: CC0-1.0\n"),
                call(f"SPDXID: {DOCUMENT_SPDX_ID}\n"),
                call("DocumentName: documentName\n"),
                call("DocumentNamespace: https://some.namespace\n"),
                call("DocumentComment: documentComment\n"),
                call("\n## External Document References\n"),
                call(
                    "ExternalDocumentRef: DocumentRef-external https://namespace.com "
                    "SHA1: 71c4025dd9897b364f3ebbb42c484ff43d00791c\n"
                ),
                call("\n"),
                call("## Creation Information\n"),
                call("LicenseListVersion: 3.19\n"),
                call("Creator: Person: creatorName (some@mail.com)\n"),
                call("Created: 2022-12-01T00:00:00Z\n"),
                call("CreatorComment: creatorComment\n"),
            ],
        ),
        (
            CreationInfo(
                spdx_version="SPDX-2.3",
                spdx_id=DOCUMENT_SPDX_ID,
                creators=[actor_fixture()],
                name="Test document",
                document_namespace="https://namespace.com",
                created=datetime.datetime(2022, 3, 10),
            ),
            [
                call("SPDXVersion: SPDX-2.3\n"),
                call("DataLicense: CC0-1.0\n"),
                call(f"SPDXID: {DOCUMENT_SPDX_ID}\n"),
                call("DocumentName: Test document\n"),
                call("DocumentNamespace: https://namespace.com\n"),
                call("\n"),
                call("## Creation Information\n"),
                call("Creator: Person: actorName (some@mail.com)\n"),
                call("Created: 2022-03-10T00:00:00Z\n"),
            ],
        ),
    ],
)
def test_creation_info_writer(creation_info, expected_calls):
    mock: MagicMock = mock_open()
    with patch(f"{__name__}.open", mock, create=True):
        with open("foo", "w") as file:
            write_creation_info(creation_info, file)

    mock.assert_called_once_with("foo", "w")
    handle = mock()
    handle.write.assert_has_calls(expected_calls)
