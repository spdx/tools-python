import re
from typing import List

from src.model.package import PackageVerificationCode
from src.validation.validation_message import ValidationMessage, ValidationContext, SpdxElementType


class PackageVerificationCodeValidator:
    spdx_version: str
    parent_id: str

    def __init__(self, spdx_version: str, parent_id: str):
        self.spdx_version = spdx_version
        self.parent_id = parent_id

    # TODO: make test for this
    def validate_verification_code(self, verification_code: PackageVerificationCode) -> List[ValidationMessage]:
        validation_messages: List[ValidationMessage] = []
        context = ValidationContext(parent_id=self.parent_id, element_type=SpdxElementType.PACKAGE_VERIFICATION_CODE,
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
