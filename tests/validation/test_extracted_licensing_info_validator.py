from typing import List

from src.model.extracted_licensing_info import ExtractedLicensingInfo
from src.validation.extracted_licensing_info_validator import ExtractedLicensingInfoValidator
from src.validation.validation_message import ValidationMessage


def test_correct_extracted_licensing_info():
    extracted_licensing_info_validator = ExtractedLicensingInfoValidator("2.3")

    extracted_licensing_info = ExtractedLicensingInfo("id", "text", "name", "comment", ["reference"])
    validation_messages: List[ValidationMessage] = extracted_licensing_info_validator.validate_extracted_licensing_info(
        extracted_licensing_info)

    assert validation_messages == []
