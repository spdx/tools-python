# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0

import re

from beartype.typing import List

from spdx_tools.spdx.model import PackageVerificationCode
from spdx_tools.spdx.validation.validation_message import SpdxElementType, ValidationContext, ValidationMessage


def validate_verification_code(verification_code: PackageVerificationCode, parent_id: str) -> List[ValidationMessage]:
    validation_messages: List[ValidationMessage] = []
    context = ValidationContext(
        parent_id=parent_id, element_type=SpdxElementType.PACKAGE_VERIFICATION_CODE, full_element=verification_code
    )

    for file in verification_code.excluded_files:
        if file.startswith("/"):
            validation_messages.append(
                ValidationMessage(f'file name must not be an absolute path starting with "/", but is: {file}', context)
            )

    value: str = verification_code.value
    if not re.match("^[0-9a-f]{40}$", value):
        validation_messages.append(
            ValidationMessage(
                f"value of verification_code must consist of 40 lowercase hexadecimal digits, but is: {value} "
                f"(length: {len(value)} digits)",
                context,
            )
        )

    return validation_messages
