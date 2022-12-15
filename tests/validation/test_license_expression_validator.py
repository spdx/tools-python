from typing import List

from src.model.license_expression import LicenseExpression
from src.validation.license_expression_validator import LicenseExpressionValidator
from src.validation.validation_message import ValidationMessage


def test_correct_license_expression():
    license_expression_validator = LicenseExpressionValidator("2.3")

    license_expression = LicenseExpression("LicenseRef-1")
    validation_messages: List[ValidationMessage] = license_expression_validator.validate_license_expression(
        license_expression)

    assert validation_messages == []
