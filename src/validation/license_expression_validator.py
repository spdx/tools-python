from typing import List, Optional, Union

from src.model.license_expression import LicenseExpression
from src.model.spdx_no_assertion import SpdxNoAssertion
from src.model.spdx_none import SpdxNone
from src.validation.validation_message import ValidationMessage


class LicenseExpressionValidator:
    spdx_version: str

    def __init__(self, spdx_version):
        self.spdx_version = spdx_version

    def validate_license_expressions(self, license_expressions: Optional[Union[List[LicenseExpression], SpdxNoAssertion, SpdxNone]]) -> List[ValidationMessage]:
        if license_expressions in [SpdxNoAssertion(), SpdxNone(), None]:
            return []

        error_messages = []

        for license_expression in license_expressions:
            error_messages.extend(self.validate_license_expression(license_expression))

        return error_messages

    def validate_license_expression(self, license_expression: LicenseExpression) -> List[ValidationMessage]:
        return []
