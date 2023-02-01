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
from license_expression import Licensing

from spdx.model.relationship import Relationship, RelationshipType
from spdx.model.spdx_no_assertion import SpdxNoAssertion
from spdx.model.spdx_none import SpdxNone
from spdx.validation.package_validator import validate_package_within_document
from spdx.validation.validation_message import ValidationMessage, ValidationContext, SpdxElementType
from tests.spdx.fixtures import package_fixture, package_verification_code_fixture, document_fixture, file_fixture


def test_valid_package():
    package = package_fixture()
    validation_messages: List[ValidationMessage] = validate_package_within_document(package, document_fixture())

    assert validation_messages == []


@pytest.mark.parametrize("package_input, expected_message",
                         [(package_fixture(files_analyzed=False, verification_code=package_verification_code_fixture(),
                                           license_info_from_files=[]),
                           f'verification_code must be None if files_analyzed is False, but is: {package_verification_code_fixture()}'),
                          (package_fixture(files_analyzed=False, license_info_from_files=SpdxNone(),
                                           verification_code=None),
                           'license_info_from_files must be None if files_analyzed is False, but is: NONE'),
                          (package_fixture(files_analyzed=False, license_info_from_files=SpdxNoAssertion(),
                                           verification_code=None),
                           'license_info_from_files must be None if files_analyzed is False, but is: NOASSERTION'),
                          (package_fixture(files_analyzed=False,
                                           license_info_from_files=[Licensing().parse("some_license")],
                                           verification_code=None),
                           "license_info_from_files must be None if files_analyzed is False, but is: [LicenseSymbol('some_license', "
                           "is_exception=False)]")
                          ])
def test_invalid_package(package_input, expected_message):
    validation_messages: List[ValidationMessage] = validate_package_within_document(package_input,
                                                                                    document_fixture(relationships=[]))

    expected = ValidationMessage(expected_message,
                                 ValidationContext(spdx_id=package_input.spdx_id, parent_id="SPDXRef-DOCUMENT",
                                                   element_type=SpdxElementType.PACKAGE,
                                                   full_element=package_input))

    assert validation_messages == [expected]


@pytest.mark.parametrize("relationships",
                         [[Relationship("SPDXRef-Package", RelationshipType.CONTAINS, "SPDXRef-File1")],
                          [Relationship("SPDXRef-Package", RelationshipType.CONTAINS, "DocumentRef-external:SPDXRef-File")],
                          [Relationship("SPDXRef-File2", RelationshipType.CONTAINED_BY, "SPDXRef-Package")],
                          [Relationship("DocumentRef-external:SPDXRef-File", RelationshipType.CONTAINED_BY, "SPDXRef-Package")],
                          [Relationship("SPDXRef-Package", RelationshipType.CONTAINS, "SPDXRef-File2"),
                           Relationship("SPDXRef-File1", RelationshipType.CONTAINED_BY, "SPDXRef-Package")]])
def test_invalid_package_with_contains(relationships):
    document = document_fixture(relationships=relationships,
                                files=[file_fixture(spdx_id="SPDXRef-File1"), file_fixture(spdx_id="SPDXRef-File2")])
    package = package_fixture(files_analyzed=False, verification_code=None, license_info_from_files=[])
    context = ValidationContext(spdx_id=package.spdx_id, parent_id=document.creation_info.spdx_id,
                                element_type=SpdxElementType.PACKAGE,
                                full_element=package)

    validation_messages: List[ValidationMessage] = validate_package_within_document(package, document)

    assert validation_messages == [
        ValidationMessage(f"package must contain no elements if files_analyzed is False, but found {relationships}",
                          context)]
