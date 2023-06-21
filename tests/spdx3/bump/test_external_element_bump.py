# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0

from unittest import TestCase

from spdx_tools.spdx3.bump_from_spdx2.checksum import bump_checksum
from spdx_tools.spdx3.bump_from_spdx2.spdx_document import bump_spdx_document
from spdx_tools.spdx3.model import ExternalMap
from spdx_tools.spdx3.payload import Payload
from spdx_tools.spdx.model import ExternalDocumentRef
from spdx_tools.spdx.model.document import Document as Spdx2_Document
from tests.spdx.fixtures import (
    checksum_fixture,
    creation_info_fixture,
    document_fixture,
    file_fixture,
    package_fixture,
    snippet_fixture,
)


def test_bump_external_elements():
    external_doc_uri = "https://external-document.uri"
    external_doc_id = "DocumentRef-external"

    full_external_doc_id = external_doc_id + ":SPDXRef-DOCUMENT"
    package_id = external_doc_id + ":SPDXRef-Package"
    file_id = external_doc_id + ":SPDXRef-File"
    snippet_id = external_doc_id + ":SPDXRef-Snippet"
    document_namespace = document_fixture().creation_info.document_namespace

    spdx2_document: Spdx2_Document = document_fixture(
        creation_info=creation_info_fixture(
            external_document_refs=[ExternalDocumentRef(external_doc_id, external_doc_uri, checksum_fixture())]
        ),
        packages=[package_fixture(spdx_id=package_id)],
        files=[file_fixture(spdx_id=file_id)],
        snippets=[snippet_fixture(spdx_id=snippet_id)],
    )
    payload: Payload = bump_spdx_document(spdx2_document)

    expected_imports = [
        ExternalMap(external_id=package_id, defining_document=full_external_doc_id),
        ExternalMap(external_id=file_id, defining_document=full_external_doc_id),
        ExternalMap(external_id=snippet_id, defining_document=full_external_doc_id),
        ExternalMap(external_id=full_external_doc_id, verified_using=[bump_checksum(checksum_fixture())]),
    ]
    spdx_document = payload.get_element(f"{document_namespace}#SPDXRef-DOCUMENT")

    assert f"{external_doc_uri}#SPDXRef-Package" in payload.get_full_map()
    assert f"{external_doc_uri}#SPDXRef-File" in payload.get_full_map()
    assert f"{external_doc_uri}#SPDXRef-Snippet" in payload.get_full_map()

    TestCase().assertCountEqual(spdx_document.imports, expected_imports)
