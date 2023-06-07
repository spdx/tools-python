# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from beartype.typing import List, Tuple

from spdx_tools.spdx3.bump_from_spdx2.checksum import bump_checksum
from spdx_tools.spdx3.model import ExternalMap, Hash, NamespaceMap
from spdx_tools.spdx.model.external_document_ref import ExternalDocumentRef


def bump_external_document_ref(external_document_ref: ExternalDocumentRef) -> Tuple[NamespaceMap, ExternalMap]:
    verified_using: List[Hash] = [bump_checksum(external_document_ref.checksum)]

    return NamespaceMap(external_document_ref.document_ref_id, external_document_ref.document_uri + "#"), ExternalMap(
        external_id=f"{external_document_ref.document_ref_id}:SPDXRef-DOCUMENT",
        verified_using=verified_using,
    )
