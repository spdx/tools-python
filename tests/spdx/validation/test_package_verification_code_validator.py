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

import pytest

from spdx.model.package import PackageVerificationCode
from spdx.validation.package_verification_code_validator import validate_verification_code
from spdx.validation.validation_message import ValidationContext, SpdxElementType, ValidationMessage


def test_valid_package_verification_code():
    code = PackageVerificationCode("71c4025dd9897b364f3ebbb42c484ff43d00791c", ["./excluded_file", "another.file"])
    validation_messages = validate_verification_code(code, "SPDXRef-Package")

    assert validation_messages == []


@pytest.mark.parametrize("code, expected_message",
                         [(PackageVerificationCode("71c4025dd9897b364f3ebbb42c484ff43d00791cab", []),
                           "value of verification_code must consist of 40 lowercase hexadecimal digits, but is: 71c4025dd9897b364f3ebbb42c484ff43d00791cab (length: 42 digits)"),
                          (PackageVerificationCode("CE9F343C4BA371746FD7EAD9B59031AE34D8AFC4", []),
                           "value of verification_code must consist of 40 lowercase hexadecimal digits, but is: CE9F343C4BA371746FD7EAD9B59031AE34D8AFC4 (length: 40 digits)"),
                          (PackageVerificationCode("71c4025dd9897b364f3ebbb42c484ff43d00791c",
                                                   ["/invalid/excluded/file"]),
                           'file name must not be an absolute path starting with "/", but is: /invalid/excluded/file')
                          ])
def test_invalid_package_verification_code(code, expected_message):
    parent_id = "SPDXRef-Package"
    context = ValidationContext(parent_id=parent_id, element_type=SpdxElementType.PACKAGE_VERIFICATION_CODE,
                                full_element=code)
    validation_messages = validate_verification_code(code, parent_id)

    assert validation_messages == [ValidationMessage(expected_message, context)]
