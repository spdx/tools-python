# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import os
from typing import List, Optional

import pytest

from spdx_tools.spdx.constants import DOCUMENT_SPDX_ID
from spdx_tools.spdx.model import CreationInfo, Document, Relationship, RelationshipType
from spdx_tools.spdx.parser.parse_anything import parse_file
from spdx_tools.spdx.validation.document_validator import validate_full_spdx_document
from spdx_tools.spdx.validation.validation_message import SpdxElementType, ValidationContext, ValidationMessage
from tests.spdx.fixtures import creation_info_fixture, document_fixture, file_fixture, package_fixture, snippet_fixture


def test_valid_document():
    document = document_fixture()
    validation_messages: List[ValidationMessage] = validate_full_spdx_document(document)

    assert validation_messages == []


def test_spdx_lite_validation():
    document = parse_file(os.path.join(os.path.dirname(__file__), "../data/SPDXLite.spdx"))

    assert validate_full_spdx_document(document) == []


@pytest.mark.parametrize(
    "creation_info, version_input, expected_message",
    [
        (creation_info_fixture(spdx_version="SPDX-2.3"), "SPDX-2.3", None),
        (creation_info_fixture(spdx_version="SPDX-2.3"), None, None),
        (
            creation_info_fixture(spdx_version="SPDX-2.3"),
            "SPDX-2.2",
            "provided SPDX version SPDX-2.2 does not match the document's SPDX version SPDX-2.3",
        ),
        (
            creation_info_fixture(spdx_version="SPDX-2.3"),
            "SPDX2.3",
            "provided SPDX version SPDX2.3 does not match the document's SPDX version SPDX-2.3",
        ),
        (
            creation_info_fixture(spdx_version="SPDX2.3"),
            "SPDX-2.3",
            'only SPDX versions "SPDX-2.2" and "SPDX-2.3" are supported, but the document\'s spdx_version is: SPDX2.3',
        ),
        (
            creation_info_fixture(spdx_version="SPDX2.3"),
            None,
            'only SPDX versions "SPDX-2.2" and "SPDX-2.3" are supported, but the document\'s spdx_version is: SPDX2.3',
        ),
        (
            creation_info_fixture(spdx_version="SPDX2.3"),
            "SPDX2.3",
            'only SPDX versions "SPDX-2.2" and "SPDX-2.3" are supported, but the document\'s spdx_version is: SPDX2.3',
        ),
        (
            creation_info_fixture(spdx_version="SPDX-2.1"),
            "SPDX-2.1",
            'only SPDX versions "SPDX-2.2" and "SPDX-2.3" are supported, but the document\'s '
            "spdx_version is: SPDX-2.1",
        ),
    ],
)
def test_spdx_version_handling(creation_info: CreationInfo, version_input: str, expected_message: Optional[str]):
    document: Document = document_fixture(creation_info=creation_info)
    validation_messages: List[ValidationMessage] = validate_full_spdx_document(document, version_input)

    context = ValidationContext(spdx_id=creation_info.spdx_id, element_type=SpdxElementType.DOCUMENT)
    expected: List[ValidationMessage] = []

    if expected_message:
        expected.append(ValidationMessage(expected_message, context))
        expected.append(
            ValidationMessage(
                "There are issues concerning the SPDX version of the document. "
                "As subsequent validation relies on the correct version, "
                "the validation process has been cancelled.",
                context,
            )
        )

    assert validation_messages == expected


@pytest.mark.parametrize(
    "relationships",
    [
        [Relationship(DOCUMENT_SPDX_ID, RelationshipType.DESCRIBES, "SPDXRef-File")],
        [Relationship("SPDXRef-File", RelationshipType.DESCRIBED_BY, DOCUMENT_SPDX_ID)],
    ],
)
def test_document_describes_at_least_one_element(relationships):
    document = document_fixture(relationships=relationships)
    validation_messages: List[ValidationMessage] = validate_full_spdx_document(document)

    assert validation_messages == []


def test_document_does_not_describe_an_element_with_only_one_package():
    document = document_fixture(
        packages=[package_fixture()],
        files=[],
        snippets=[],
        relationships=[],
        annotations=[],
    )
    validation_messages: List[ValidationMessage] = validate_full_spdx_document(document)

    assert validation_messages == []


def test_document_does_not_describe_an_element_with_multiple_elements():
    document = document_fixture(
        relationships=[Relationship("SPDXRef-Package", RelationshipType.DESCRIBES, "SPDXRef-File")]
    )
    validation_messages: List[ValidationMessage] = validate_full_spdx_document(document)

    assert validation_messages == [
        ValidationMessage(
            f'there must be at least one relationship "{DOCUMENT_SPDX_ID} DESCRIBES ..." or "... DESCRIBED_BY '
            f'{DOCUMENT_SPDX_ID}" when there is not only a single package present',
            ValidationContext(spdx_id=DOCUMENT_SPDX_ID, element_type=SpdxElementType.DOCUMENT),
        )
    ]


def test_duplicated_spdx_ids():
    document = document_fixture(
        files=[
            file_fixture(spdx_id="SPDXRef-File"),
            file_fixture(spdx_id="SPDXRef-2"),
            file_fixture(spdx_id="SPDXRef-3"),
        ],
        packages=[package_fixture(spdx_id="SPDXRef-2"), package_fixture(spdx_id=DOCUMENT_SPDX_ID)],
        snippets=[snippet_fixture(spdx_id="SPDXRef-2"), snippet_fixture(spdx_id="SPDXRef-3")],
    )

    context = ValidationContext(spdx_id=document.creation_info.spdx_id, element_type=SpdxElementType.DOCUMENT)

    validation_messages: List[ValidationMessage] = validate_full_spdx_document(document)

    assert validation_messages == [
        ValidationMessage(
            "every spdx_id must be unique within the document, but found the following duplicates: ['SPDXRef-2', "
            f"'SPDXRef-3', '{DOCUMENT_SPDX_ID}']",
            context,
        )
    ]
