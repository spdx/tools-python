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

from typing import List

import pytest

from spdx.model.checksum import Checksum, ChecksumAlgorithm
from spdx.validation.file_validator import validate_file_within_document
from spdx.validation.validation_message import ValidationMessage, ValidationContext, SpdxElementType
from tests.spdx.fixtures import file_fixture, document_fixture


def test_valid_file():
    file = file_fixture()
    validation_messages: List[ValidationMessage] = validate_file_within_document(file, document_fixture())

    assert validation_messages == []


@pytest.mark.parametrize("file_input, spdx_id, expected_message",
                         [(file_fixture(name="/invalid/file/name"), file_fixture().spdx_id,
                           f'file name must not be an absolute path starting with "/", but is: /invalid/file/name'),
                         (
                          file_fixture(checksums=[Checksum(ChecksumAlgorithm.MD2, "d4c41ce30a517d6ce9d79c8c17bb4b66")]),
                          file_fixture().spdx_id,
                          f'checksums must contain a SHA1 algorithm checksum, but only contains: [<ChecksumAlgorithm.MD2: 13>]')
                          ])
def test_invalid_file(file_input, spdx_id, expected_message):
    validation_messages: List[ValidationMessage] = validate_file_within_document(file_input, document_fixture())

    expected = ValidationMessage(expected_message,
                                 ValidationContext(spdx_id=spdx_id,
                                                   parent_id=document_fixture().creation_info.spdx_id,
                                                   element_type=SpdxElementType.FILE,
                                                   full_element=file_input))

    assert validation_messages == [expected]
