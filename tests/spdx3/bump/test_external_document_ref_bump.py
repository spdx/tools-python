# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0

from spdx_tools.spdx3.bump_from_spdx2.checksum import bump_checksum
from spdx_tools.spdx3.bump_from_spdx2.creation_info import bump_creation_info
from spdx_tools.spdx3.bump_from_spdx2.external_document_ref import bump_external_document_ref
from spdx_tools.spdx3.payload import Payload
from spdx_tools.spdx.model import ExternalDocumentRef
from tests.spdx.fixtures import checksum_fixture, creation_info_fixture, external_document_ref_fixture


def test_bump_external_document_ref():
    checksum = checksum_fixture()
    external_document_ref = ExternalDocumentRef("DocumentRef-external", "https://external.uri", checksum)
    namespace_map, imports = bump_external_document_ref(external_document_ref)

    assert namespace_map.prefix == "DocumentRef-external"
    assert namespace_map.namespace == "https://external.uri#"

    assert imports.external_id == "DocumentRef-external:SPDXRef-DOCUMENT"
    assert imports.verified_using == [bump_checksum(checksum)]


def test_bump_multiple_external_document_refs():
    payload = Payload()
    creation_info = creation_info_fixture(
        external_document_refs=[
            external_document_ref_fixture("DocumentRef-external1", "https://external.uri1"),
            external_document_ref_fixture("DocumentRef-external2", "https://external.uri2"),
        ]
    )
    spdx_document = bump_creation_info(creation_info, payload)

    assert len(spdx_document.imports) == 2
    assert len(spdx_document.namespaces) == 2
