# Copyright (c) 2022 spdx contributors
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

from src.model.checksum import Checksum, ChecksumAlgorithm
from src.model.file import FileType
from src.model.license_expression import LicenseExpression
from src.parser.error import SPDXParsingError
from src.parser.json.file_parser import FileParser


def test_file_parser():
    file_parser = FileParser()
    file_dict = {
        "SPDXID": "SPDXRef-File",
        "attributionTexts": ["Some attribution text."],
        "checksums": [{
            "algorithm": "SHA1",
            "checksumValue": "d6a770ba38583ed4bb4525bd96e50461655d2758"
        }, {
            "algorithm": "MD5",
            "checksumValue": "624c1abb3664f4b35547e7c73864ad24"
        }],
        "comment": "The concluded license was taken from the package level that the file was included in.\nThis information was found in the COPYING.txt file in the xyz directory.",
        "copyrightText": "Copyright 2008-2010 John Smith",
        "fileContributors": ["The Regents of the University of California",
                             "Modified by Paul Mundt lethal@linux-sh.org", "IBM Corporation"],
        "fileName": "./package/foo.c",
        "fileTypes": ["SOURCE"],
        "licenseComments": "The concluded license was taken from the package level that the file was included in.",
        "licenseConcluded": "(LGPL-2.0-only OR LicenseRef-2)",
        "licenseInfoInFiles": ["GPL-2.0-only", "LicenseRef-2"],
        "noticeText": "Copyright (c) 2001 Aaron Lehmann aaroni@vitelus.com\n\nPermission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the \"Software\"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions: \nThe above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."
    }

    file = file_parser.parse_file(file_dict)

    assert file.name == "./package/foo.c"
    assert file.spdx_id == "SPDXRef-File"
    assert file.checksums == [Checksum(ChecksumAlgorithm.SHA1, "d6a770ba38583ed4bb4525bd96e50461655d2758"),
                              Checksum(ChecksumAlgorithm.MD5, "624c1abb3664f4b35547e7c73864ad24")]
    assert file.comment == "The concluded license was taken from the package level that the file was included in.\nThis information was found in the COPYING.txt file in the xyz directory."
    assert file.copyright_text == "Copyright 2008-2010 John Smith"
    assert file.file_type == [FileType.SOURCE]
    assert file.contributors == ["The Regents of the University of California",
                                 "Modified by Paul Mundt lethal@linux-sh.org", "IBM Corporation"]
    assert file.concluded_license == LicenseExpression("(LGPL-2.0-only OR LicenseRef-2)")
    assert file.license_info_in_file == [LicenseExpression("GPL-2.0-only"), LicenseExpression("LicenseRef-2")]
    assert file.license_comment == "The concluded license was taken from the package level that the file was included in."
    assert file.attribution_texts == ["Some attribution text."]


def test_parse_incomplete_file():
    file_parser = FileParser()
    file_dict = {
        "SPDXID": "SPDXRef-File",
        "fileName": "Incomplete File"
    }

    with pytest.raises(SPDXParsingError) as err:
        _ = file_parser.parse_file(file_dict)

    assert err.type == SPDXParsingError
    assert err.value.messages == ["Error while parsing file Incomplete File: ['No checksums provided, checksums are "
                                  "mandatory for files.']"]


def test_parse_falsy_files():
    file_parser = FileParser()
    files = [{"SPDXID": "SPDXRef-File",
              "fileName": "Incomplete File"},
             {"SPDXID": "SPDXRef-File",
              "attributionTexts": ["Some attribution text."],
              "checksums": [{
                  "algorithm": "SHA1",
                  "checksumValue": "d6a770ba38583ed4bb4525bd96e50461655d2758"
              }, {
                  "algorithm": "MD5",
                  "checksumValue": "624c1abb3664f4b35547e7c73864ad24"
              }]},
             {"SPDXID": "SPDXRef-File",
              "attributionTexts": ["Some attribution text."],
              "checksums": [{
                  "algorithm": "SHA1",
                  "checksumValue": "d6a770ba38583ed4bb4525bd96e50461655d2758"
              }, {
                  "algorithm": "MD",
                  "checksumValue": "624c1abb3664f4b35547e7c73864ad24"
              }]},
             ]

    with pytest.raises(SPDXParsingError) as err:
        _ = file_parser.parse_files(files)

    assert err.type == SPDXParsingError
    assert err.value.messages == ["Error while parsing file Incomplete File: ['No checksums provided, checksums "
                                  "are mandatory for files.']",
                                  "Error while constructing file None: ['SetterError File: type of argument "
                                  '"name" must be str; got NoneType instead: None\']',
                                  'Error while parsing file None: ["Error while parsing checksum: [\'Algorithm '
                                  'MD not valid for checksum.\']"]']

def test_parse_file_types():
    file_parser = FileParser()
    file_types_list = ["OTHER", "APPLICATION"]

    file_types = file_parser.parse_file_types(file_types_list)

    assert file_types == [FileType.OTHER, FileType.APPLICATION]

def test_parse_invalid_file_types():
    file_parser = FileParser()
    file_types_list = ["OTHER", "APPLICAON"]

    with pytest.raises(SPDXParsingError) as err:
        _ = file_parser.parse_file_types(file_types_list)

    assert err.type == SPDXParsingError
    assert err.value.messages == ["Error while parsing file_types: ['FileType APPLICAON is not valid.']"]
