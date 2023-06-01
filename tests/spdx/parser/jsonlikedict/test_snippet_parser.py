# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from unittest import TestCase

import pytest
from license_expression import Licensing

from spdx_tools.spdx.model import SpdxNoAssertion, SpdxNone
from spdx_tools.spdx.parser.error import SPDXParsingError
from spdx_tools.spdx.parser.jsonlikedict.snippet_parser import SnippetParser


@pytest.mark.parametrize(
    "copyright_text, expected_copyright_text",
    [
        ("Copyright 2008-2010 John Smith", "Copyright 2008-2010 John Smith"),
        ("NOASSERTION", SpdxNoAssertion()),
        ("NONE", SpdxNone()),
    ],
)
def test_parse_snippet(copyright_text, expected_copyright_text):
    snippet_parser = SnippetParser()

    snippet_dict = {
        "SPDXID": "SPDXRef-Snippet",
        "comment": "This snippet was identified as significant and highlighted in this Apache-2.0 file, when a "
        "commercial scanner identified it as being derived from file foo.c in package xyz which is licensed"
        " under GPL-2.0.",
        "copyrightText": copyright_text,
        "licenseComments": "The concluded license was taken from package xyz, from which the snippet was copied into "
        "the current file. The concluded license information was found in the COPYING.txt file in "
        "package xyz.",
        "licenseConcluded": "GPL-2.0-only",
        "licenseInfoInSnippets": ["GPL-2.0-only", "NOASSERTION"],
        "name": "from linux kernel",
        "ranges": [
            {
                "endPointer": {"offset": 420, "reference": "SPDXRef-DoapSource"},
                "startPointer": {"offset": 310, "reference": "SPDXRef-DoapSource"},
            },
            {
                "endPointer": {"lineNumber": 23, "reference": "SPDXRef-DoapSource"},
                "startPointer": {"lineNumber": 5, "reference": "SPDXRef-DoapSource"},
            },
        ],
        "snippetFromFile": "SPDXRef-DoapSource",
        "attributionTexts": ["Some example attibution text."],
    }
    snippet = snippet_parser.parse_snippet(snippet_dict)

    assert snippet.spdx_id == "SPDXRef-Snippet"
    assert snippet.name == "from linux kernel"
    assert (
        snippet.comment
        == "This snippet was identified as significant and highlighted in this Apache-2.0 file, when a commercial "
        "scanner identified it as being derived from file foo.c in package xyz which is licensed under GPL-2.0."
    )
    assert snippet.copyright_text == expected_copyright_text
    assert (
        snippet.license_comment
        == "The concluded license was taken from package xyz, from which the snippet was copied into the current file."
        " The concluded license information was found in the COPYING.txt file in package xyz."
    )
    assert snippet.byte_range == (310, 420)
    assert snippet.line_range == (5, 23)
    assert snippet.file_spdx_id == "SPDXRef-DoapSource"
    assert snippet.license_info_in_snippet == [Licensing().parse("GPL-2.0-only"), SpdxNoAssertion()]
    assert snippet.license_concluded == Licensing().parse("GPL-2.0-only")
    assert snippet.attribution_texts == ["Some example attibution text."]


def test_parse_incomplete_snippet():
    snippet_parser = SnippetParser()
    incomplete_snippet_dict = {"SPDXID": "SPDXRef-Snippet", "file_spdx_id": "SPDXRef-File"}

    with pytest.raises(SPDXParsingError):
        snippet_parser.parse_snippet(incomplete_snippet_dict)


def test_parse_snippet_with_invalid_snippet_range():
    snippet_parser = SnippetParser()
    snippet_with_invalid_ranges_list = {
        "SPDXID": "SPDXRef-Snippet",
        "file_spdx_id": "SPDXRef-File",
        "ranges": [
            {
                "endPointer": {"offset": 23, "reference": "SPDXRef-DoapSource"},
                "startPointer": {"offset": "310s", "reference": "SPDXRef-DoapSource"},
            }
        ],
    }

    with pytest.raises(SPDXParsingError):
        snippet_parser.parse_snippet(snippet_with_invalid_ranges_list)


def test_parse_invalid_snippet_range():
    snippet_parser = SnippetParser()

    ranges = [
        {
            "endPointer": {"lineNumber": 23, "reference": "SPDXRef-DoapSource"},
            "startPointer": {"offset": 310, "reference": "SPDXRef-DoapSource"},
        },
        {
            "endPointer": {"offset": 420, "reference": "SPDXRef-DoapSource"},
            "startPointer": {"lineNumber": 5, "reference": "SPDXRef-DoapSource"},
        },
    ]

    with pytest.raises(SPDXParsingError) as err:
        snippet_parser.parse_ranges(ranges)

    TestCase().assertCountEqual(
        err.value.get_messages(),
        [
            "Error while parsing snippet ranges: ['Type of startpointer is not the same as type of endpointer.', "
            "'Type of startpointer is not the same as type of endpointer.']"
        ],
    )
