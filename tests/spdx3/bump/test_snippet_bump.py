# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from unittest import mock

from spdx_tools.spdx3.bump_from_spdx2.snippet import bump_snippet
from spdx_tools.spdx3.model.licensing import ConjunctiveLicenseSet, ListedLicense
from spdx_tools.spdx3.model.software import Snippet
from spdx_tools.spdx3.payload import Payload
from spdx_tools.spdx.model.snippet import Snippet as Spdx2_Snippet
from tests.spdx.fixtures import snippet_fixture


@mock.patch("spdx_tools.spdx3.model.CreationInfo", autospec=True)
def test_bump_snippet(creation_info):
    payload = Payload()
    document_namespace = "https://doc.namespace"
    spdx2_snippet: Spdx2_Snippet = snippet_fixture()
    expected_new_snippet_id = f"{document_namespace}#{spdx2_snippet.spdx_id}"

    bump_snippet(spdx2_snippet, payload, creation_info, document_namespace, [], [], [])
    snippet = payload.get_element(expected_new_snippet_id)

    assert isinstance(snippet, Snippet)
    assert snippet.spdx_id == expected_new_snippet_id
    assert snippet.copyright_text == spdx2_snippet.copyright_text
    assert snippet.attribution_text == spdx2_snippet.attribution_texts[0]
    assert snippet.concluded_license == ConjunctiveLicenseSet(
        [ListedLicense("MIT", "MIT", ""), ListedLicense("GPL-2.0-only", "GPL-2.0-only", "")]
    )
