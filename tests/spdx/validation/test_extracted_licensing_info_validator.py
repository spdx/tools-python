# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0

from typing import List

import pytest

from spdx_tools.spdx.validation.extracted_licensing_info_validator import validate_extracted_licensing_info
from spdx_tools.spdx.validation.validation_message import SpdxElementType, ValidationContext, ValidationMessage
from tests.spdx.fixtures import extracted_licensing_info_fixture


def test_valid_extracted_licensing_info():
    extracted_licensing_info = extracted_licensing_info_fixture()
    validation_messages: List[ValidationMessage] = validate_extracted_licensing_info(extracted_licensing_info)

    assert validation_messages == []


# TODO: tests for licenses not on the SPDX License list (i.e. they must provide id, name and cross-references)
@pytest.mark.parametrize(
    "extracted_licensing_info, expected_message",
    [
        (
            extracted_licensing_info_fixture(extracted_text=None),
            "extracted_text must be provided if there is a license_id assigned",
        ),
        (
            extracted_licensing_info_fixture(cross_references=["invalid_url"]),
            "cross_reference must be a valid URL, but is: invalid_url",
        ),
    ],
)
def test_invalid_extracted_licensing_info(extracted_licensing_info, expected_message):
    validation_messages: List[ValidationMessage] = validate_extracted_licensing_info(extracted_licensing_info)

    expected = ValidationMessage(
        expected_message,
        ValidationContext(
            element_type=SpdxElementType.EXTRACTED_LICENSING_INFO, full_element=extracted_licensing_info
        ),
    )

    assert validation_messages == [expected]
