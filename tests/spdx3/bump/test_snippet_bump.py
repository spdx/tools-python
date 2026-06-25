# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0

from spdx_tools.spdx3.bump_from_spdx2.snippet import bump_snippet
from spdx_tools.spdx3.model.creation_info import CreationInfo
from spdx_tools.spdx3.model.software import Snippet
from spdx_tools.spdx3.payload import Payload
from spdx_tools.spdx.model import File
from spdx_tools.spdx.model.snippet import Snippet as Spdx2_Snippet
from tests.spdx3.fixtures import creation_info_fixture
from tests.spdx.fixtures import file_fixture, snippet_fixture


def test_bump_snippet():
    payload = Payload()
    document_namespace = "https://doc.namespace"
    spdx2_snippet: Spdx2_Snippet = snippet_fixture()
    spdx2_file: File = file_fixture()
    expected_new_snippet_id = f"{document_namespace}#{spdx2_snippet.spdx_id}"
    expected_new_snippet_file_id = f"{document_namespace}#{spdx2_file.spdx_id}"
    creation_info: CreationInfo = creation_info_fixture()

    bump_snippet(spdx2_snippet, spdx2_file, payload, document_namespace, [], [], creation_info)
    snippet = payload.get_element(expected_new_snippet_id)

    assert isinstance(snippet, Snippet)
    assert snippet.spdx_id == expected_new_snippet_id
    assert snippet.snippet_from_file == expected_new_snippet_file_id
    assert snippet.copyright_text == spdx2_snippet.copyright_text
    assert snippet.attribution_text == spdx2_snippet.attribution_texts
