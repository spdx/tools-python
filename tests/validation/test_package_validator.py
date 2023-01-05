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

from src.model.license_expression import LicenseExpression
from src.model.spdx_no_assertion import SpdxNoAssertion
from src.model.spdx_none import SpdxNone
from src.validation.package_validator import validate_package_within_document
from src.validation.validation_message import ValidationMessage, ValidationContext, SpdxElementType
from tests.fixtures import package_fixture, package_verification_code_fixture, document_fixture


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
                                           license_info_from_files=[LicenseExpression("some_license")],
                                           verification_code=None),
                           'license_info_from_files must be None if files_analyzed is False, but is: [LicenseExpression(expression_string=\'some_license\')]')
                          ])
def test_invalid_package(package_input, expected_message):
    validation_messages: List[ValidationMessage] = validate_package_within_document(package_input,
                                                                                    document_fixture(relationships=[]))

    expected = ValidationMessage(expected_message,
                                 ValidationContext(spdx_id=package_input.spdx_id, parent_id="SPDXRef-DOCUMENT",
                                                   element_type=SpdxElementType.PACKAGE,
                                                   full_element=package_input))

    assert validation_messages == [expected]
