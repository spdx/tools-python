from typing import List

import pytest

from src.model.extracted_licensing_info import ExtractedLicensingInfo
from src.validation.extracted_licensing_info_validator import ExtractedLicensingInfoValidator
from src.validation.validation_message import ValidationMessage, ValidationContext, SpdxElementType


def test_correct_extracted_licensing_info():
    extracted_licensing_info_validator = ExtractedLicensingInfoValidator("2.3")

    extracted_licensing_info = ExtractedLicensingInfo("LicenseRef-1", "extracted text", "license name", "comment", ["reference"])
    validation_messages: List[ValidationMessage] = extracted_licensing_info_validator.validate_extracted_licensing_info(
        extracted_licensing_info)

    assert validation_messages == []
    
    
@pytest.mark.parametrize("extracted_licensing_info, expected_message",
                         [(get_extracted_licensing_info(extracted_licensing_info_type=Extracted_licensing_infoType.TOOL, mail="mail@mail.com"),
                           'email must be None if extracted_licensing_info_type is TOOL, but is: mail@mail.com'),
                          ])
def test_wrong_extracted_licensing_info(extracted_licensing_info, expected_message):
    parent_id = "SPDXRef-DOCUMENT"
    extracted_licensing_info_validator = Extracted_licensing_infoValidator("2.3", parent_id)
    validation_messages: List[ValidationMessage] = extracted_licensing_info_validator.validate_extracted_licensing_info(extracted_licensing_info)

    expected = ValidationMessage(expected_message,
                                 ValidationContext(parent_id=parent_id, element_type=SpdxElementType.EXTRACTED_LICENSING_INFO,
                                                   full_element=extracted_licensing_info))

    assert validation_messages == [expected]

