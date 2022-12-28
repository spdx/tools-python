#  Copyright (c) 2022 spdx contributors
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#      http://www.apache.org/licenses/LICENSE-2.0
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import re
from typing import List

from src.model.package import PackageVerificationCode
from src.validation.validation_message import ValidationMessage, ValidationContext, SpdxElementType


# TODO: make test for this (https://github.com/spdx/tools-python/issues/386)
def validate_verification_code(verification_code: PackageVerificationCode, parent_id: str) -> List[ValidationMessage]:
    validation_messages: List[ValidationMessage] = []
    context = ValidationContext(parent_id=parent_id, element_type=SpdxElementType.PACKAGE_VERIFICATION_CODE,
                                full_element=verification_code)

    for file in verification_code.excluded_files:
        if not file.startswith("./"):
            validation_messages.append(
                ValidationMessage(
                    f'file name must be a relative path to the file, starting with "./", but is: {file}', context)
            )

    value: str = verification_code.value
    if not re.match("^[0-9a-f]{40}$", value):
        validation_messages.append(
            ValidationMessage(
                f"value of verification_code must consist of 40 hexadecimal digits, but is: {value} (length: {len(value)} digits)",
                context)
        )

    return validation_messages
