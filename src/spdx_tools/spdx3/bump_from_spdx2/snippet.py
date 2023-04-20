# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from spdx_tools.spdx3.bump_from_spdx2.message import print_missing_conversion
from spdx_tools.spdx3.model import CreationInformation
from spdx_tools.spdx3.model.software import Snippet
from spdx_tools.spdx3.payload import Payload
from spdx_tools.spdx.model.snippet import Snippet as Spdx2_Snippet


def bump_snippet(
    spdx2_snippet: Spdx2_Snippet, payload: Payload, creation_information: CreationInformation, document_namespace: str
):
    spdx_id = "#".join([document_namespace, spdx2_snippet.spdx_id])
    print_missing_conversion("snippet.file_spdx_id", 0)
    byte_range = spdx2_snippet.byte_range
    line_range = spdx2_snippet.line_range
    print_missing_conversion(
        "snippet.concluded_license, snippet.license_info_in_snippet, snippet.license_comment,"
        "snippet.copyright_text",
        0,
        "missing definitions for license profile",
    )
    comment = spdx2_snippet.comment
    name = spdx2_snippet.name

    print_missing_conversion("snippet.attribution_texts", 0, "missing definitions for license profile")

    payload.add_element(
        Snippet(
            spdx_id=spdx_id,
            creation_info=creation_information,
            byte_range=byte_range,
            line_range=line_range,
            comment=comment,
            name=name,
        )
    )
