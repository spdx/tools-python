# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from unittest import mock

from spdx3.bump_from_spdx2.snippet import bump_snippet
from spdx3.model.software.snippet import Snippet
from spdx3.payload import Payload
from spdx.model.snippet import Snippet as Spdx2_Snippet
from tests.spdx.fixtures import snippet_fixture


@mock.patch("spdx3.model.creation_information.CreationInformation", autospec=True)
def test_bump_snippet(creation_information):
    payload = Payload()
    document_namespace = "https://doc.namespace"
    spdx2_snippet: Spdx2_Snippet = snippet_fixture()
    expected_new_snippet_id = f"{document_namespace}#{spdx2_snippet.spdx_id}"

    bump_snippet(spdx2_snippet, payload, creation_information, document_namespace)
    snippet = payload.get_element(expected_new_snippet_id)

    assert isinstance(snippet, Snippet)
    assert snippet.spdx_id == expected_new_snippet_id
