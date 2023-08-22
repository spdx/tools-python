# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from unittest import TestCase

import pytest

from spdx_tools.common.spdx_licensing import spdx_licensing
from spdx_tools.spdx.model import SpdxNoAssertion
from spdx_tools.spdx.parser.error import SPDXParsingError
from spdx_tools.spdx.parser.tagvalue.parser import Parser
from tests.spdx.parser.tagvalue.test_creation_info_parser import DOCUMENT_STR


def test_parse_snippet():
    parser = Parser()
    snippet_str = "\n".join(
        [
            "SnippetSPDXID: SPDXRef-Snippet",
            "SnippetLicenseComments: <text>Some lic comment.</text>",
            "SnippetCopyrightText: <text> Copyright 2008-2010 John Smith </text>",
            "SnippetComment: <text>Some snippet comment.</text>",
            "SnippetName: from linux kernel",
            "SnippetFromFileSPDXID: SPDXRef-DoapSource",
            "SnippetLicenseConcluded: Apache-2.0",
            "LicenseInfoInSnippet: NOASSERTION",
            "SnippetByteRange: 310:420",
            "SnippetLineRange: 5:23",
            "SnippetAttributionText: <text>This is a text\nthat spans multiple lines.</text>",
            "SnippetAttributionText:   This text spans one line but has trailing and leading whitespaces.      ",
        ]
    )

    document = parser.parse("\n".join([DOCUMENT_STR, snippet_str]))
    assert document is not None
    assert len(document.snippets) == 1
    snippet = document.snippets[0]
    assert snippet.spdx_id == "SPDXRef-Snippet"
    assert snippet.name == "from linux kernel"
    assert snippet.comment == "Some snippet comment."
    assert snippet.copyright_text == " Copyright 2008-2010 John Smith "
    assert snippet.license_comment == "Some lic comment."
    assert snippet.file_spdx_id == "SPDXRef-DoapSource"
    assert snippet.license_concluded == spdx_licensing.parse("Apache-2.0")
    assert snippet.license_info_in_snippet == [SpdxNoAssertion()]
    assert snippet.byte_range[0] == 310
    assert snippet.byte_range[1] == 420
    assert snippet.line_range[0] == 5
    assert snippet.line_range[1] == 23
    TestCase().assertCountEqual(
        snippet.attribution_texts,
        [
            "This is a text\nthat spans multiple lines.",
            "This text spans one line but has trailing and leading whitespaces.",
        ],
    )


@pytest.mark.parametrize(
    "snippet_str, expected_message",
    [
        (
            "SnippetName: TestSnippet",
            "Element Snippet is not the current element in scope, probably the expected "
            "tag to start the element (SnippetSPDXID) is missing. Line: 1",
        ),
        (
            "SnippetSPDXID: SPDXDRef-Snippet\nSnippetByteRange: 1,4",
            "Error while parsing Snippet: [\"Value for SnippetByteRange doesn't match "
            'valid range pattern. Line: 2"]',
        ),
        (
            "SnippetSPDXID: SPDXDRef-Snippet\nSnippetByteRange: 1:4\nSnippetByteRange:10:23",
            "Error while parsing Snippet: ['Multiple values for SnippetByteRange found. " "Line: 3']",
        ),
        (
            "SnippetSPDXID: SPDXRef-Snippet",
            r"__init__() missing 2 required " r"positional arguments: 'file_spdx_id' and 'byte_range'",
        ),
    ],
)
def test_parse_invalid_snippet(snippet_str, expected_message):
    parser = Parser()

    with pytest.raises(SPDXParsingError) as err:
        parser.parse(snippet_str)

    assert expected_message in err.value.get_messages()[0]
