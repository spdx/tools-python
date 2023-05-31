# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0

from unittest import mock

from spdx_tools.spdx.model import ExternalDocumentRef


@mock.patch("spdx_tools.spdx.model.Checksum", autospec=True)
def test_correct_initialization(checksum):
    external_document_ref = ExternalDocumentRef("id", "uri", checksum)
    assert external_document_ref.document_ref_id == "id"
    assert external_document_ref.document_uri == "uri"
    assert external_document_ref.checksum == checksum
