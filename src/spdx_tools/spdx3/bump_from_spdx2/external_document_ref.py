# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from typing import List

from spdx_tools.spdx3.bump_from_spdx2.checksum import bump_checksum
from spdx_tools.spdx3.model import ExternalMap, Hash
from spdx_tools.spdx.model.external_document_ref import ExternalDocumentRef


def bump_external_document_ref(external_document_ref: ExternalDocumentRef) -> ExternalMap:
    external_id: str = external_document_ref.document_ref_id
    verified_using: List[Hash] = [bump_checksum(external_document_ref.checksum)]
    location_hint: str = external_document_ref.document_uri

    return ExternalMap(external_id, verified_using, location_hint)
