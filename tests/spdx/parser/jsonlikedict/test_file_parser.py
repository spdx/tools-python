# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from unittest import TestCase

import pytest
from license_expression import Licensing

from spdx_tools.spdx.model import Checksum, ChecksumAlgorithm, FileType, SpdxNoAssertion, SpdxNone
from spdx_tools.spdx.parser.error import SPDXParsingError
from spdx_tools.spdx.parser.jsonlikedict.dict_parsing_functions import parse_list_of_elements
from spdx_tools.spdx.parser.jsonlikedict.file_parser import FileParser


@pytest.mark.parametrize(
    "copyright_text, expected_copyright_text",
    [
        ("Copyright 2008-2010 John Smith", "Copyright 2008-2010 John Smith"),
        ("NOASSERTION", SpdxNoAssertion()),
        ("NONE", SpdxNone()),
    ],
)
def test_parse_file(copyright_text, expected_copyright_text):
    file_parser = FileParser()
    file_dict = {
        "SPDXID": "SPDXRef-File",
        "attributionTexts": ["Some attribution text."],
        "checksums": [
            {"algorithm": "SHA1", "checksumValue": "d6a770ba38583ed4bb4525bd96e50461655d2758"},
            {"algorithm": "MD5", "checksumValue": "624c1abb3664f4b35547e7c73864ad24"},
        ],
        "comment": "The concluded license was taken from the package level that the file was included in.\nThis "
        "information was found in the COPYING.txt file in the xyz directory.",
        "copyrightText": copyright_text,
        "fileContributors": [
            "The Regents of the University of California",
            "Modified by Paul Mundt lethal@linux-sh.org",
            "IBM Corporation",
        ],
        "fileName": "./package/foo.c",
        "fileTypes": ["SOURCE"],
        "licenseComments": "The concluded license was taken from the package level that the file was included in.",
        "licenseConcluded": "(LGPL-2.0-only OR LicenseRef-2)",
        "licenseInfoInFiles": ["GPL-2.0-only", "LicenseRef-2", "NOASSERTION"],
        "noticeText": "Copyright (c) 2001 Aaron Lehmann aaroni@vitelus.com\n\nPermission is hereby granted, free of "
        "charge, to any person obtaining a copy of this software and associated documentation files "
        '(the "Software"), to deal in the Software without restriction, including without limitation '
        "the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of "
        "the Software, and to permit persons to whom the Software is furnished to do so, subject to the "
        "following conditions: \nThe above copyright notice and this permission notice shall be "
        "included in all copies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "
        '"AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE '
        "WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO "
        "EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER "
        "LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN "
        "CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.",
    }

    file = file_parser.parse_file(file_dict)

    assert file.name == "./package/foo.c"
    assert file.spdx_id == "SPDXRef-File"
    TestCase().assertCountEqual(
        file.checksums,
        [
            Checksum(ChecksumAlgorithm.SHA1, "d6a770ba38583ed4bb4525bd96e50461655d2758"),
            Checksum(ChecksumAlgorithm.MD5, "624c1abb3664f4b35547e7c73864ad24"),
        ],
    )
    assert (
        file.comment
        == "The concluded license was taken from the package level that the file was included in.\nThis information "
        "was found in the COPYING.txt file in the xyz directory."
    )
    assert file.copyright_text == expected_copyright_text
    assert file.file_types == [FileType.SOURCE]
    TestCase().assertCountEqual(
        file.contributors,
        [
            "The Regents of the University of California",
            "Modified by Paul Mundt lethal@linux-sh.org",
            "IBM Corporation",
        ],
    )
    assert file.license_concluded == Licensing().parse("(LGPL-2.0-only OR LicenseRef-2)")
    TestCase().assertCountEqual(
        file.license_info_in_file,
        [Licensing().parse("GPL-2.0-only"), Licensing().parse("LicenseRef-2"), SpdxNoAssertion()],
    )
    assert (
        file.license_comment == "The concluded license was taken from the package level that the file was included in."
    )
    assert file.attribution_texts == ["Some attribution text."]


def test_parse_invalid_files():
    file_parser = FileParser()
    files = [
        {"SPDXID": "SPDXRef-File", "fileName": "Incomplete File"},
        {
            "SPDXID": "SPDXRef-File",
            "attributionTexts": ["Some attribution text."],
            "checksums": [
                {"algorithm": "SHA1", "checksumValue": "d6a770ba38583ed4bb4525bd96e50461655d2758"},
                {"algorithm": "MD5", "checksumValue": "624c1abb3664f4b35547e7c73864ad24"},
            ],
        },
        {
            "SPDXID": "SPDXRef-File",
            "attributionTexts": ["Some attribution text."],
            "checksums": [
                {"algorithm": "SHA1", "checksumValue": "d6a770ba38583ed4bb4525bd96e50461655d2758"},
                {"algorithm": "MD", "checksumValue": "624c1abb3664f4b35547e7c73864ad24"},
            ],
        },
        {"SPDXID": "SPDXRef-File", "fileName": "Incomplete File"},
    ]

    with pytest.raises(SPDXParsingError):
        parse_list_of_elements(files, file_parser.parse_file)


def test_parse_file_types():
    file_parser = FileParser()
    file_types_list = ["OTHER", "APPLICATION"]

    file_types = file_parser.parse_file_types(file_types_list)

    TestCase().assertCountEqual(file_types, [FileType.OTHER, FileType.APPLICATION])


def test_parse_invalid_file_types():
    file_parser = FileParser()
    file_types_list = ["OTHER", "APPLICAON"]

    with pytest.raises(SPDXParsingError) as err:
        file_parser.parse_file_types(file_types_list)

    TestCase().assertCountEqual(
        err.value.get_messages(), ["Error while parsing FileType: ['Invalid FileType: APPLICAON']"]
    )
