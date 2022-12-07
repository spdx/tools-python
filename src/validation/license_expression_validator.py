from typing import List

from src.model.license_expression import LicenseExpression
from src.validation.validation_message import ValidationMessage


class LicenseExpressionValidator:
    spdx_version: str
    
    def __init__(self, spdx_version):
        self.spdx_version = spdx_version

    def validate_license_expressions(self, license_expressions: List[LicenseExpression]) -> List[ValidationMessage]:
        error_messages = []
        for license_expression in license_expressions:
            error_messages.extend(self.validate_license_expression(license_expression))

        return error_messages

    def validate_license_expression(self, license_expression: LicenseExpression) -> ValidationMessage:
        pass
