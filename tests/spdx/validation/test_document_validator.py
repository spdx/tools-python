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
from spdx.model.relationship import Relationship, RelationshipType
from spdx.validation.document_validator import validate_full_spdx_document
from spdx.validation.validation_message import ValidationMessage, ValidationContext, SpdxElementType
from tests.spdx.fixtures import document_fixture, creation_info_fixture, file_fixture, package_fixture, snippet_fixture


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
                           'only SPDX versions "SPDX-2.2" and "SPDX-2.3" are supported, but the document\'s spdx_version is: SPDX2.3'),
                          (creation_info_fixture(spdx_version="SPDX2.3"), None,
                           'only SPDX versions "SPDX-2.2" and "SPDX-2.3" are supported, but the document\'s spdx_version is: SPDX2.3'),
                          (creation_info_fixture(spdx_version="SPDX2.3"), "SPDX2.3",
                           'only SPDX versions "SPDX-2.2" and "SPDX-2.3" are supported, but the document\'s spdx_version is: SPDX2.3'),
                          (creation_info_fixture(spdx_version="SPDX-2.1"), "SPDX-2.1",
                           'only SPDX versions "SPDX-2.2" and "SPDX-2.3" are supported, but the document\'s spdx_version is: SPDX-2.1'),
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


@pytest.mark.parametrize("relationships",
                         [[Relationship("SPDXRef-DOCUMENT", RelationshipType.DESCRIBES, "SPDXRef-File")],
                          [Relationship("SPDXRef-File", RelationshipType.DESCRIBED_BY, "SPDXRef-DOCUMENT")]])
def test_document_describes_at_least_one_element(relationships):
    document = document_fixture(relationships=relationships)
    validation_messages: List[ValidationMessage] = validate_full_spdx_document(document)

    assert validation_messages == []


def test_document_does_not_describe_an_element():
    document = document_fixture(
        relationships=[Relationship("SPDXRef-Package", RelationshipType.DESCRIBES, "SPDXRef-File")])
    validation_messages: List[ValidationMessage] = validate_full_spdx_document(document)

    assert validation_messages == [ValidationMessage(
        'there must be at least one relationship "SPDXRef-DOCUMENT DESCRIBES ..." or "... DESCRIBED_BY SPDXRef-DOCUMENT"',
        ValidationContext(spdx_id="SPDXRef-DOCUMENT", element_type=SpdxElementType.DOCUMENT)
    )]


def test_duplicated_spdx_ids():
    document = document_fixture(
        files=[file_fixture(spdx_id="SPDXRef-File"), file_fixture(spdx_id="SPDXRef-2"),
               file_fixture(spdx_id="SPDXRef-3")],
        packages=[package_fixture(spdx_id="SPDXRef-2"), package_fixture(spdx_id="SPDXRef-DOCUMENT")],
        snippets=[snippet_fixture(spdx_id="SPDXRef-2"), snippet_fixture(spdx_id="SPDXRef-3")])

    context = ValidationContext(spdx_id=document.creation_info.spdx_id, element_type=SpdxElementType.DOCUMENT)

    validation_messages: List[ValidationMessage] = validate_full_spdx_document(document)

    assert validation_messages == [ValidationMessage(
        "every spdx_id must be unique within the document, but found the following duplicates: ['SPDXRef-2', 'SPDXRef-3', 'SPDXRef-DOCUMENT']",
        context)]
