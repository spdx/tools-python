from typing import List, Optional, Union

from src.model.license_expression import LicenseExpression
from src.model.spdx_no_assertion import SpdxNoAssertion
from src.model.spdx_none import SpdxNone
from src.validation.validation_message import ValidationMessage


def validate_license_expressions(license_expressions: Optional[
    Union[List[LicenseExpression], SpdxNoAssertion, SpdxNone]]) -> List[ValidationMessage]:
    if license_expressions in [SpdxNoAssertion(), SpdxNone(), None]:
        return []

    error_messages = []

    for license_expression in license_expressions:
        error_messages.extend(validate_license_expression(license_expression))

    return error_messages


def validate_license_expression(license_expression: LicenseExpression) -> List[ValidationMessage]:
    # TODO: implement this once we have a better license expression model: https://github.com/spdx/tools-python/issues/374
    return []
