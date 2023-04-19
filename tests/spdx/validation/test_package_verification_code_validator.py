# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0

import pytest

from spdx_tools.spdx.model import PackageVerificationCode
from spdx_tools.spdx.validation.package_verification_code_validator import validate_verification_code
from spdx_tools.spdx.validation.validation_message import SpdxElementType, ValidationContext, ValidationMessage


def test_valid_package_verification_code():
    code = PackageVerificationCode("71c4025dd9897b364f3ebbb42c484ff43d00791c", ["./excluded_file", "another.file"])
    validation_messages = validate_verification_code(code, "SPDXRef-Package")

    assert validation_messages == []


@pytest.mark.parametrize(
    "code, expected_message",
    [
        (
            PackageVerificationCode("71c4025dd9897b364f3ebbb42c484ff43d00791cab", []),
            "value of verification_code must consist of 40 lowercase hexadecimal digits, but is: "
            "71c4025dd9897b364f3ebbb42c484ff43d00791cab (length: 42 digits)",
        ),
        (
            PackageVerificationCode("CE9F343C4BA371746FD7EAD9B59031AE34D8AFC4", []),
            "value of verification_code must consist of 40 lowercase hexadecimal digits, but is: "
            "CE9F343C4BA371746FD7EAD9B59031AE34D8AFC4 (length: 40 digits)",
        ),
        (
            PackageVerificationCode("71c4025dd9897b364f3ebbb42c484ff43d00791c", ["/invalid/excluded/file"]),
            'file name must not be an absolute path starting with "/", but is: /invalid/excluded/file',
        ),
    ],
)
def test_invalid_package_verification_code(code, expected_message):
    parent_id = "SPDXRef-Package"
    context = ValidationContext(
        parent_id=parent_id, element_type=SpdxElementType.PACKAGE_VERIFICATION_CODE, full_element=code
    )
    validation_messages = validate_verification_code(code, parent_id)

    assert validation_messages == [ValidationMessage(expected_message, context)]
