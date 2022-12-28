#  Copyright (c) 2022 spdx contributors
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#      http://www.apache.org/licenses/LICENSE-2.0
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from typing import List

import pytest

from src.model.checksum import Checksum, ChecksumAlgorithm
from src.model.file import File, FileType
from src.model.spdx_no_assertion import SpdxNoAssertion
from src.model.spdx_none import SpdxNone
from src.validation.file_validator import validate_file_within_document
from src.validation.validation_message import ValidationMessage, ValidationContext, SpdxElementType
from tests.valid_defaults import get_checksum, get_file, get_document


def test_valid_file():
    file = File("./file/name.py", "SPDXRef-File", [get_checksum()], [FileType.OTHER, FileType.SPDX], SpdxNone(),
                SpdxNoAssertion(),
                "comment on license", "copyright", "comment", "notice", ["contributor"], ["attribution"])
    validation_messages: List[ValidationMessage] = validate_file_within_document(file, get_document())

    assert validation_messages == []


@pytest.mark.parametrize("file_input, spdx_id, expected_message",
                         [(get_file(name="invalid file name"), get_file().spdx_id,
                           'file name must be a relative path to the file, starting with "./", but is: invalid file name'),
                          (get_file(checksums=[Checksum(ChecksumAlgorithm.MD2, "d4c41ce30a517d6ce9d79c8c17bb4b66")]),
                           get_file().spdx_id,
                           f'checksums must contain a SHA1 algorithm checksum, but only contains: [<ChecksumAlgorithm.MD2: 13>]')
                          ])
def test_invalid_file(file_input, spdx_id, expected_message):
    validation_messages: List[ValidationMessage] = validate_file_within_document(file_input, get_document())

    expected = ValidationMessage(expected_message,
                                 ValidationContext(spdx_id=spdx_id,
                                                   parent_id=get_document().creation_info.spdx_id,
                                                   element_type=SpdxElementType.FILE,
                                                   full_element=file_input))

    assert validation_messages == [expected]
