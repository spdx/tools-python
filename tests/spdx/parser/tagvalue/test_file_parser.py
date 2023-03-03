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

from spdx.model.file import FileType
from spdx.model.spdx_no_assertion import SpdxNoAssertion
from spdx.parser.error import SPDXParsingError
from spdx.parser.tagvalue.parser import Parser
from tests.spdx.parser.tagvalue.test_creation_info_parser import DOCUMENT_STR


def test_parse_file():
    parser = Parser()
    file_str = "\n".join([
        "FileName: testfile.java",
        "SPDXID: SPDXRef-File",
        "FileType: SOURCE",
        "FileType: TEXT",
        "FileChecksum: SHA1: 2fd4e1c67a2d28fced849ee1bb76e7391b93eb12",
        "LicenseConcluded: Apache-2.0",
        "LicenseInfoInFile: Apache-2.0",
        "LicenseInfoInFile: NOASSERTION",
        "FileCopyrightText: <text>Copyright 2014 Acme Inc.</text>",
        "FileComment: <text>Very long file</text>",
        "FileAttributionText: <text>Acknowledgements that might be required to be communicated in some contexts.</text>"
    ])
    document = parser.parse("\n".join([DOCUMENT_STR, file_str]))
    assert document is not None
    assert len(document.files) == 1
    spdx_file = document.files[0]
    assert spdx_file.name == "testfile.java"
    assert spdx_file.spdx_id == "SPDXRef-File"
    assert spdx_file.file_types == [FileType.SOURCE, FileType.TEXT]
    assert spdx_file.comment == "Very long file"
    assert spdx_file.attribution_texts == [
        "Acknowledgements that might be required to be communicated in some contexts."]
    assert spdx_file.license_info_in_file == [get_spdx_licensing().parse("Apache-2.0"),
                                              SpdxNoAssertion()]
    assert spdx_file.license_concluded == get_spdx_licensing().parse("Apache-2.0")


def test_parse_invalid_file():
    parser = Parser()
    file_str = "\n".join([
        "FileName: testfile.java",
        "SPDXID: SPDXRef-File",
        "FileType: SOUCE",
        "FileType: TEXT",
        "FileChecksum: SHA3: 2fd4e1c67a2d28fced849ee1bb76e7391b93eb12",
        "LicenseConcluded: Apache-2.0",
        "LicenseInfoInFile: Apache-2.0",
        "FileCopyrightText: <text>Copyright 2014 Acme Inc.</text>",
        "FileComment: <text>Very long file</text>",
        "FileAttributionText: <text>Acknowledgements that might be required to be communicated in some contexts.</text>"
    ])

    with pytest.raises(SPDXParsingError) as err:
        parser.parse(file_str)

    assert err.value.get_messages() == [
        "Error while parsing File: ['Invalid FileType: SOUCE. Line 3', 'Error while "
        "parsing FileChecksum: Token did not match specified grammar rule. Line: 5']"]
