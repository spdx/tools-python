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

from spdx.model.document import Document
from spdx.model.relationship import Relationship, RelationshipType
from spdx.model.spdx_no_assertion import SpdxNoAssertion
from spdx.model.spdx_none import SpdxNone
from spdx.validation.relationship_validator import validate_relationship
from spdx.validation.validation_message import ValidationMessage, SpdxElementType, ValidationContext
from tests.spdx.fixtures import document_fixture, relationship_fixture


@pytest.mark.parametrize("related_spdx_element",
                         ["SPDXRef-Package", SpdxNoAssertion(), SpdxNone()])
def test_valid_relationship(related_spdx_element):
    relationship = Relationship("SPDXRef-DOCUMENT", RelationshipType.DESCRIBES, related_spdx_element, comment="comment")
    validation_messages: List[ValidationMessage] = validate_relationship(relationship, "SPDX-2.3", document_fixture())

    assert validation_messages == []


@pytest.mark.parametrize("spdx_element_id, related_spdx_element_id, expected_message",
                         [("SPDXRef-unknownFile", "SPDXRef-File",
                           'did not find the referenced spdx_id "SPDXRef-unknownFile" in the SPDX document'),
                          ("SPDXRef-File", "SPDXRef-unknownFile",
                           'did not find the referenced spdx_id "SPDXRef-unknownFile" in the SPDX document'),
                          ])
def test_unknown_spdx_id(spdx_element_id, related_spdx_element_id, expected_message):
    relationship: Relationship = relationship_fixture(spdx_element_id=spdx_element_id,
                                                      related_spdx_element_id=related_spdx_element_id)
    validation_messages: List[ValidationMessage] = validate_relationship(relationship, "SPDX-2.3", document_fixture())

    expected = ValidationMessage(expected_message,
                                 ValidationContext(element_type=SpdxElementType.RELATIONSHIP,
                                                   full_element=relationship))

    assert validation_messages == [expected]


@pytest.mark.parametrize("relationship, expected_message",
                         [(Relationship("SPDXRef-DOCUMENT", RelationshipType.SPECIFICATION_FOR, "SPDXRef-Package"),
                           "RelationshipType.SPECIFICATION_FOR is not supported in SPDX-2.2"),
                          (Relationship("SPDXRef-DOCUMENT", RelationshipType.REQUIREMENT_DESCRIPTION_FOR,
                                        "SPDXRef-Package"),
                           "RelationshipType.REQUIREMENT_DESCRIPTION_FOR is not supported in SPDX-2.2")])
def test_v2_3_only_types(relationship, expected_message):
    document: Document = document_fixture()

    validation_message: List[ValidationMessage] = validate_relationship(relationship, "SPDX-2.2", document)

    expected = [ValidationMessage(expected_message,
                                  ValidationContext(element_type=SpdxElementType.RELATIONSHIP,
                                                    full_element=relationship))]

    assert validation_message == expected
