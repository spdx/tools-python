# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from typing import List

from spdx_tools.spdx3.bump_from_spdx2.checksum import bump_checksum
from spdx_tools.spdx3.bump_from_spdx2.external_element_utils import get_full_element_spdx_id_and_set_imports
from spdx_tools.spdx3.bump_from_spdx2.license_expression import bump_license_expression_or_none_or_no_assertion
from spdx_tools.spdx3.bump_from_spdx2.message import print_missing_conversion
from spdx_tools.spdx3.model import CreationInfo, ExternalMap
from spdx_tools.spdx3.model.software import File
from spdx_tools.spdx3.payload import Payload
from spdx_tools.spdx.model import ExternalDocumentRef, ExtractedLicensingInfo, SpdxNoAssertion
from spdx_tools.spdx.model.file import File as Spdx2_File


def bump_file(
    spdx2_file: Spdx2_File,
    payload: Payload,
    creation_info: CreationInfo,
    document_namespace: str,
    extracted_licensing_info: List[ExtractedLicensingInfo],
    external_document_refs: List[ExternalDocumentRef],
    imports: List[ExternalMap],
):
    spdx_id = get_full_element_spdx_id_and_set_imports(spdx2_file, document_namespace, external_document_refs, imports)

    integrity_methods = [bump_checksum(checksum) for checksum in spdx2_file.checksums]
    print_missing_conversion(
        "file.file_type", 0, "different cardinalities, " "https://github.com/spdx/spdx-3-model/issues/82"
    )
    license_concluded = bump_license_expression_or_none_or_no_assertion(
        spdx2_file.license_concluded, extracted_licensing_info
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
            creation_info=creation_info,
            name=spdx2_file.name,
            comment=spdx2_file.comment,
            verified_using=integrity_methods,
            concluded_license=license_concluded,
            copyright_text=copyright_text,
            attribution_text=", ".join(spdx2_file.attribution_texts),
        )
    )
