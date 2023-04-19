# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0

from typing import List

import pytest

from spdx_tools.spdx.constants import DOCUMENT_SPDX_ID
from spdx_tools.spdx.model import Document, Relationship, RelationshipType, SpdxNoAssertion, SpdxNone
from spdx_tools.spdx.validation.relationship_validator import validate_relationship
from spdx_tools.spdx.validation.validation_message import SpdxElementType, ValidationContext, ValidationMessage
from tests.spdx.fixtures import document_fixture, relationship_fixture


@pytest.mark.parametrize("related_spdx_element", ["SPDXRef-Package", SpdxNoAssertion(), SpdxNone()])
def test_valid_relationship(related_spdx_element):
    relationship = Relationship(DOCUMENT_SPDX_ID, RelationshipType.DESCRIBES, related_spdx_element, comment="comment")
    validation_messages: List[ValidationMessage] = validate_relationship(relationship, "SPDX-2.3", document_fixture())

    assert validation_messages == []


@pytest.mark.parametrize(
    "spdx_element_id, related_spdx_element_id, expected_message",
    [
        (
            "SPDXRef-unknownFile",
            "SPDXRef-File",
            'did not find the referenced spdx_id "SPDXRef-unknownFile" in the SPDX document',
        ),
        (
            "SPDXRef-File",
            "SPDXRef-unknownFile",
            'did not find the referenced spdx_id "SPDXRef-unknownFile" in the SPDX document',
        ),
    ],
)
def test_unknown_spdx_id(spdx_element_id, related_spdx_element_id, expected_message):
    relationship: Relationship = relationship_fixture(
        spdx_element_id=spdx_element_id, related_spdx_element_id=related_spdx_element_id
    )
    validation_messages: List[ValidationMessage] = validate_relationship(relationship, "SPDX-2.3", document_fixture())

    expected = ValidationMessage(
        expected_message, ValidationContext(element_type=SpdxElementType.RELATIONSHIP, full_element=relationship)
    )

    assert validation_messages == [expected]


@pytest.mark.parametrize(
    "relationship, expected_message",
    [
        (
            Relationship(DOCUMENT_SPDX_ID, RelationshipType.SPECIFICATION_FOR, "SPDXRef-Package"),
            "RelationshipType.SPECIFICATION_FOR is not supported in SPDX-2.2",
        ),
        (
            Relationship(DOCUMENT_SPDX_ID, RelationshipType.REQUIREMENT_DESCRIPTION_FOR, "SPDXRef-Package"),
            "RelationshipType.REQUIREMENT_DESCRIPTION_FOR is not supported in SPDX-2.2",
        ),
    ],
)
def test_v2_3_only_types(relationship, expected_message):
    document: Document = document_fixture()

    validation_message: List[ValidationMessage] = validate_relationship(relationship, "SPDX-2.2", document)

    expected = [
        ValidationMessage(
            expected_message, ValidationContext(element_type=SpdxElementType.RELATIONSHIP, full_element=relationship)
        )
    ]

    assert validation_message == expected
