from typing import List

from src.model.license_expression import LicenseExpression
from src.validation.license_expression_validator import validate_license_expression
from src.validation.validation_message import ValidationMessage


def test_valid_license_expression():
    license_expression = LicenseExpression("LicenseRef-1")
    validation_messages: List[ValidationMessage] = validate_license_expression(license_expression)

    assert validation_messages == []
