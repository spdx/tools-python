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

from typing import List

import pytest

from src.model.extracted_licensing_info import ExtractedLicensingInfo
from src.validation.extracted_licensing_info_validator import validate_extracted_licensing_info
from src.validation.validation_message import ValidationMessage, ValidationContext, SpdxElementType
from tests.valid_defaults import get_extracted_licensing_info


def test_valid_extracted_licensing_info():
    extracted_licensing_info = ExtractedLicensingInfo("LicenseRef-1", "extracted text", "license name",
                                                      ["http://some.url"], "comment")
    validation_messages: List[ValidationMessage] = validate_extracted_licensing_info(extracted_licensing_info)

    assert validation_messages == []


# TODO: tests for licenses not on the SPDX License list (i.e. they must provide id, name and cross-references)
@pytest.mark.parametrize("extracted_licensing_info, expected_message",
                         [(get_extracted_licensing_info(extracted_text=None),
                           'extracted_text must be provided if there is a license_id assigned'),
                          (get_extracted_licensing_info(cross_references=["invalid_url"]),
                           'cross_reference must be a valid URL, but is: invalid_url')
                          ])
def test_invalid_extracted_licensing_info(extracted_licensing_info, expected_message):
    validation_messages: List[ValidationMessage] = validate_extracted_licensing_info(extracted_licensing_info)

    expected = ValidationMessage(expected_message,
                                 ValidationContext(element_type=SpdxElementType.EXTRACTED_LICENSING_INFO,
                                                   full_element=extracted_licensing_info))

    assert validation_messages == [expected]
