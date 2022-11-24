from typing import List

import pytest

from src.model.document import Document
from src.model.relationship import Relationship, RelationshipType
from src.validation.relationship_validator import RelationshipValidator
from src.validation.validation_message import ValidationMessage, SpdxElementType, ValidationContext
from tests.valid_defaults import get_document, get_package, get_relationship, get_file


def test_correct_relationship():
    document: Document = get_document(packages=[get_package(spdx_id="SPDXRef-Package")])
    relationship_validator = RelationshipValidator("2.3", document)

    relationship = Relationship("SPDXRef-DOCUMENT", RelationshipType.AMENDS, "SPDXRef-Package", comment="comment")
    validation_messages: List[ValidationMessage] = relationship_validator.validate_relationship(relationship)

    assert validation_messages == []


@pytest.mark.parametrize("first_id, second_id, wrong_file_id, expected_message",
                         [("SPDXRef-some_file", "SPDXRef-File", "SPDXRef-some_file",
                           'spdx_id must only contain letters, numbers, "." and "-" and must begin with "SPDXRef-", but is: SPDXRef-some_file'),
                          ("SPDXRef-File", "SPDXRef-some_file", "SPDXRef-some_file",
                           'spdx_id must only contain letters, numbers, "." and "-" and must begin with "SPDXRef-", but is: SPDXRef-some_file'),
                          ("SPDXRef-unknownFile", "SPDXRef-hiddenFile", "SPDXRef-hiddenFile",
                           'did not find the referenced spdx_id SPDXRef-unknownFile in the SPDX document'),
                          ("SPDXRef-hiddenFile", "SPDXRef-unknownFile", "SPDXRef-hiddenFile",
                           'did not find the referenced spdx_id SPDXRef-unknownFile in the SPDX document'),
                          ])
def test_wrong_relationship(first_id, second_id, wrong_file_id, expected_message):
    relationship: Relationship = get_relationship(spdx_element_id=first_id, related_spdx_element_id=second_id)
    document: Document = get_document(files=[get_file(spdx_id="SPDXRef-File"), get_file(spdx_id=wrong_file_id)])
    relationship_validator = RelationshipValidator("2.3", document)
    validation_messages: List[ValidationMessage] = relationship_validator.validate_relationship(relationship)

    expected = ValidationMessage(expected_message,
                                 ValidationContext(element_type=SpdxElementType.RELATIONSHIP,
                                                   full_element=relationship))

    assert validation_messages == [expected]


@pytest.mark.parametrize("relationship, expected_message",
                         [(Relationship("SPDXRef-DOCUMENT", RelationshipType.SPECIFICATION_FOR, "SPDXRef-Package"),
                           "RelationshipType.SPECIFICATION_FOR is not supported for SPDX versions below 2.3"),
                          (Relationship("SPDXRef-DOCUMENT", RelationshipType.REQUIREMENT_DESCRIPTION_FOR,
                                        "SPDXRef-Package"),
                           "RelationshipType.REQUIREMENT_DESCRIPTION_FOR is not supported for SPDX versions below 2.3")])
def test_v2_3_only_types(relationship, expected_message):
    document: Document = get_document(packages=[get_package(spdx_id="SPDXRef-Package")])
    relationship_validator = RelationshipValidator("2.2", document)

    validation_message: List[ValidationMessage] = relationship_validator.validate_relationship(relationship)

    expected = [ValidationMessage(expected_message,
                                  ValidationContext(element_type=SpdxElementType.RELATIONSHIP,
                                                    full_element=relationship))]

    assert validation_message == expected
