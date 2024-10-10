# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from beartype.typing import List

from . import bump_positive_integer_range, print_missing_conversion
from ..model.core import ExternalMap
from ..model.software import Snippet
from ..payload import Payload
from ...spdx.model import ExternalDocumentRef, SpdxNoAssertion
from ...spdx.model.snippet import Snippet as Spdx2_Snippet
from ...spdx.spdx_element_utils import get_full_element_spdx_id


def bump_snippet(
    spdx2_snippet: Spdx2_Snippet,
    payload: Payload,
    document_namespace: str,
    external_document_refs: List[ExternalDocumentRef],
    import_: List[ExternalMap],
):
    spdx_id = get_full_element_spdx_id(spdx2_snippet, document_namespace, external_document_refs)
    if ":" in spdx2_snippet.spdx_id:
        import_.append(
            ExternalMap(
                external_id=spdx2_snippet.spdx_id,
                defining_document=f"{spdx2_snippet.spdx_id.split(':')[0]}:SPDXRef-DOCUMENT",
            )
        )

    print_missing_conversion("snippet.file_spdx_id", 0, "https://github.com/spdx/spdx-3-model/issues/130")
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
            name=spdx2_snippet.name,
            comment=spdx2_snippet.comment,
            byte_range=bump_positive_integer_range(spdx2_snippet.byte_range),
            line_range=bump_positive_integer_range(spdx2_snippet.line_range),
            copyright_text=copyright_text,
            attribution_text=", ".join(spdx2_snippet.attribution_texts),
        )
    )
