# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from beartype.typing import List

from spdx_tools.spdx3.bump_from_spdx2.checksum import bump_checksum
from spdx_tools.spdx3.bump_from_spdx2.message import print_missing_conversion
from spdx_tools.spdx3.model import ExternalMap
from spdx_tools.spdx3.model.software import File
from spdx_tools.spdx3.payload import Payload
from spdx_tools.spdx.model import ExternalDocumentRef, SpdxNoAssertion
from spdx_tools.spdx.model.file import File as Spdx2_File
from spdx_tools.spdx.spdx_element_utils import get_full_element_spdx_id


def bump_file(
    spdx2_file: Spdx2_File,
    payload: Payload,
    document_namespace: str,
    external_document_refs: List[ExternalDocumentRef],
    imports: List[ExternalMap],
):
    spdx_id = get_full_element_spdx_id(spdx2_file, document_namespace, external_document_refs)
    if ":" in spdx2_file.spdx_id:
        imports.append(
            ExternalMap(
                external_id=spdx2_file.spdx_id,
                defining_document=f"{spdx2_file.spdx_id.split(':')[0]}:SPDXRef-DOCUMENT",
            )
        )

    integrity_methods = [bump_checksum(checksum) for checksum in spdx2_file.checksums]
    print_missing_conversion(
        "file.file_type", 0, "different cardinalities, " "https://github.com/spdx/spdx-3-model/issues/82"
    )
    copyright_text = None
    if isinstance(spdx2_file.copyright_text, str):
        copyright_text = spdx2_file.copyright_text
    elif isinstance(spdx2_file.copyright_text, SpdxNoAssertion):
        print_missing_conversion("package2.copyright_text", 0)
    print_missing_conversion(
        "file.notice, file.contributors, file.license_info_in_file, file.license_comment",
        0,
        "missing definition for license profile",
    )

    payload.add_element(
        File(
            spdx_id,
            name=spdx2_file.name,
            comment=spdx2_file.comment,
            verified_using=integrity_methods,
            copyright_text=copyright_text,
            attribution_text=", ".join(spdx2_file.attribution_texts),
        )
    )
