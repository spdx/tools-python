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

from typing import List, Optional

import pytest

from spdx.model.document import Document, CreationInfo
from spdx.validation.document_validator import validate_full_spdx_document
from spdx.validation.validation_message import ValidationMessage, ValidationContext, SpdxElementType
from tests.fixtures import document_fixture, creation_info_fixture


def test_valid_document():
    document = document_fixture()
    validation_messages: List[ValidationMessage] = validate_full_spdx_document(document)

    assert validation_messages == []


@pytest.mark.parametrize("creation_info, version_input, expected_message",
                         [(creation_info_fixture(spdx_version="SPDX-2.3"), "SPDX-2.3", None),
                          (creation_info_fixture(spdx_version="SPDX-2.3"), None, None),
                          (creation_info_fixture(spdx_version="SPDX-2.3"), "SPDX-2.2",
                           "provided SPDX version SPDX-2.2 does not match the document's SPDX version SPDX-2.3"),
                          (creation_info_fixture(spdx_version="SPDX-2.3"), "SPDX2.3",
                           "provided SPDX version SPDX2.3 does not match the document's SPDX version SPDX-2.3"),
                          (creation_info_fixture(spdx_version="SPDX2.3"), "SPDX-2.3",
                           'the document\'s spdx_version must be of the form "SPDX-[major].[minor]" but is: SPDX2.3'),
                          (creation_info_fixture(spdx_version="SPDX2.3"), None,
                           'the document\'s spdx_version must be of the form "SPDX-[major].[minor]" but is: SPDX2.3'),
                          (creation_info_fixture(spdx_version="SPDX2.3"), "SPDX2.3",
                           'the document\'s spdx_version must be of the form "SPDX-[major].[minor]" but is: SPDX2.3'),
                          ])
def test_spdx_version_handling(creation_info: CreationInfo, version_input: str, expected_message: Optional[str]):
    document: Document = document_fixture(creation_info=creation_info)
    validation_messages: List[ValidationMessage] = validate_full_spdx_document(document, version_input)

    context = ValidationContext(spdx_id=creation_info.spdx_id, element_type=SpdxElementType.DOCUMENT)
    expected: List[ValidationMessage] = []

    if expected_message:
        expected.append(ValidationMessage(expected_message, context))
        expected.append(ValidationMessage("There are issues concerning the SPDX version of the document. "
                                          "As subsequent validation relies on the correct version, "
                                          "the validation process has been cancelled.", context))

    assert validation_messages == expected

    # TODO: https://github.com/spdx/tools-python/issues/375
