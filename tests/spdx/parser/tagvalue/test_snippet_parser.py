# Copyright (c) 2023 spdx contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import pytest
from license_expression import get_spdx_licensing

from spdx.parser.tagvalue.parser.tagvalue import Parser
from tests.spdx.parser.tagvalue.test_creation_info_parser import DOCUMENT_STR


@pytest.fixture
def parser():
    spdx_parser = Parser()
    spdx_parser.build()
    return spdx_parser


def test_snippet(parser):
    snippet_str = '\n'.join([
        'SnippetSPDXID: SPDXRef-Snippet',
        'SnippetLicenseComments: <text>Some lic comment.</text>',
        'SnippetCopyrightText: <text> Copyright 2008-2010 John Smith </text>',
        'SnippetComment: <text>Some snippet comment.</text>',
        'SnippetName: from linux kernel',
        'SnippetFromFileSPDXID: SPDXRef-DoapSource',
        'SnippetLicenseConcluded: Apache-2.0',
        'LicenseInfoInSnippet: Apache-2.0',
        'SnippetByteRange: 310:420',
        'SnippetLineRange: 5:23',
    ])

    document = parser.parse("\n".join([DOCUMENT_STR, snippet_str]))
    assert document is not None
    assert len(document.snippets) == 1
    snippet = document.snippets[0]
    assert snippet.spdx_id == 'SPDXRef-Snippet'
    assert snippet.name == 'from linux kernel'
    assert snippet.comment == 'Some snippet comment.'
    assert snippet.copyright_text == ' Copyright 2008-2010 John Smith '
    assert snippet.license_comment == 'Some lic comment.'
    assert snippet.file_spdx_id == 'SPDXRef-DoapSource'
    assert snippet.license_concluded == get_spdx_licensing().parse('Apache-2.0')
    assert snippet.license_info_in_snippet == [get_spdx_licensing().parse('Apache-2.0')]
    assert snippet.byte_range[0] == 310
    assert snippet.byte_range[1] == 420
    assert snippet.line_range[0] == 5
    assert snippet.line_range[1] == 23
