# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from typing import List

from spdx_tools.spdx3.bump_from_spdx2.external_element_utils import get_full_element_spdx_id_and_set_imports
from spdx_tools.spdx3.bump_from_spdx2.license_expression import bump_license_expression_or_none_or_no_assertion
from spdx_tools.spdx3.bump_from_spdx2.message import print_missing_conversion
from spdx_tools.spdx3.model import CreationInfo, ExternalMap
from spdx_tools.spdx3.model.software import Snippet
from spdx_tools.spdx3.payload import Payload
from spdx_tools.spdx.model import ExternalDocumentRef, ExtractedLicensingInfo, SpdxNoAssertion
from spdx_tools.spdx.model.snippet import Snippet as Spdx2_Snippet


def bump_snippet(
    spdx2_snippet: Spdx2_Snippet,
    payload: Payload,
    creation_info: CreationInfo,
    document_namespace: str,
    extracted_licensing_info: List[ExtractedLicensingInfo],
    external_document_refs: List[ExternalDocumentRef],
    imports: List[ExternalMap],
):
    spdx_id = get_full_element_spdx_id_and_set_imports(
        spdx2_snippet, document_namespace, external_document_refs, imports
    )

    print_missing_conversion("snippet.file_spdx_id", 0, "https://github.com/spdx/spdx-3-model/issues/130")
    concluded_license = bump_license_expression_or_none_or_no_assertion(
        spdx2_snippet.license_concluded, extracted_licensing_info
    )
    copyright_text = None
    if isinstance(spdx2_snippet.copyright_text, str):
        copyright_text = spdx2_snippet.copyright_text
    elif isinstance(spdx2_snippet.copyright_text, SpdxNoAssertion):
        print_missing_conversion("package2.copyright_text", 0)
    print_missing_conversion(
        "snippet.license_info_in_snippet, snippet.license_comment,",
        0,
        "missing definitions for license profile",
    )

    payload.add_element(
        Snippet(
            spdx_id=spdx_id,
            creation_info=creation_info,
            name=spdx2_snippet.name,
            comment=spdx2_snippet.comment,
            byte_range=spdx2_snippet.byte_range,
            line_range=spdx2_snippet.line_range,
            copyright_text=copyright_text,
            attribution_text=", ".join(spdx2_snippet.attribution_texts),
            concluded_license=concluded_license,
        )
    )
