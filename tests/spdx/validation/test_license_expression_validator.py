# Copyright (c) 2022 spdx contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import List
from unittest import TestCase

import pytest
from license_expression import get_spdx_licensing, LicenseExpression

from spdx.model.document import Document
from spdx.model.spdx_no_assertion import SpdxNoAssertion
from spdx.model.spdx_none import SpdxNone
from spdx.validation.license_expression_validator import validate_license_expression, validate_license_expressions
from spdx.validation.validation_message import ValidationMessage, ValidationContext, SpdxElementType
from tests.spdx.fixtures import document_fixture, extracted_licensing_info_fixture


FIXTURE_LICENSE_ID = extracted_licensing_info_fixture().license_id


@pytest.mark.parametrize("expression_string",
                         ["MIT", FIXTURE_LICENSE_ID,
                          f"GPL-2.0-only with GPL-CC-1.0 and {FIXTURE_LICENSE_ID} with 389-exception or Beerware"])
def test_valid_license_expression(expression_string):
    document: Document = document_fixture()
    license_expression: LicenseExpression = get_spdx_licensing().parse(expression_string)
    validation_messages: List[ValidationMessage] = validate_license_expression(license_expression, document,
                                                                               parent_id="SPDXRef-File")

    assert validation_messages == []


@pytest.mark.parametrize("expression", [SpdxNone(), SpdxNoAssertion()])
def test_none_and_no_assertion(expression):
    document: Document = document_fixture()
    validation_messages: List[ValidationMessage] = validate_license_expression(expression, document,
                                                                               parent_id="SPDXRef-File")
    assert validation_messages == []


@pytest.mark.parametrize("expression_list",
                         [[SpdxNone()], [SpdxNoAssertion()],
                          [get_spdx_licensing().parse("MIT and GPL-3.0-only"),
                           get_spdx_licensing().parse(FIXTURE_LICENSE_ID)],
                          [SpdxNone(), get_spdx_licensing().parse("MIT"), SpdxNoAssertion()]
                          ])
def test_valid_license_expressions(expression_list):
    document: Document = document_fixture()
    validation_messages: List[ValidationMessage] = validate_license_expressions(expression_list, document,
                                                                                parent_id="SPDXRef-File")
    assert validation_messages == []


@pytest.mark.parametrize("expression_string, unknown_symbols",
                         [(f"{FIXTURE_LICENSE_ID} or LicenseRef-22", ["LicenseRef-22"]),
                          ("nope with 389-exception and _.- or LicenseRef-10", ["nope", "_.-", "LicenseRef-10"])
                          ])
def test_invalid_license_expression_with_unknown_symbols(expression_string, unknown_symbols):
    document: Document = document_fixture()
    license_expression: LicenseExpression = get_spdx_licensing().parse(expression_string)
    parent_id = "SPDXRef-File"
    context = ValidationContext(parent_id=parent_id, element_type=SpdxElementType.LICENSE_EXPRESSION,
                                full_element=license_expression)

    validation_messages: List[ValidationMessage] = validate_license_expression(license_expression, document, parent_id)
    expected_messages = [ValidationMessage(
        f"Unrecognized license reference: {symbol}. license_expression must only use IDs from the license list or extracted licensing info, but is: {license_expression}",
        context
    ) for symbol in unknown_symbols]

    TestCase().assertCountEqual(validation_messages, expected_messages)


@pytest.mark.parametrize("expression_string, expected_message",
                         [("MIT with MIT",
                           'A plain license symbol cannot be used as an exception in a "WITH symbol" statement. for token: "MIT" at position: 9. for license_expression: MIT WITH MIT'),
                          (f"GPL-2.0-or-later and {FIXTURE_LICENSE_ID} with {FIXTURE_LICENSE_ID}",
                           f'A plain license symbol cannot be used as an exception in a "WITH symbol" statement. for token: "{FIXTURE_LICENSE_ID}" at position: 39. for license_expression: GPL-2.0-or-later AND {FIXTURE_LICENSE_ID} WITH {FIXTURE_LICENSE_ID}'),
                          (f"GPL-2.0-or-later with MIT and {FIXTURE_LICENSE_ID} with GPL-2.0-or-later",
                           f'A plain license symbol cannot be used as an exception in a "WITH symbol" statement. for token: "MIT" at position: 22. for license_expression: GPL-2.0-or-later WITH MIT AND {FIXTURE_LICENSE_ID} WITH GPL-2.0-or-later'),
                          ("389-exception with 389-exception",
                           'A license exception symbol can only be used as an exception in a "WITH exception" statement. for token: "389-exception". for license_expression: 389-exception WITH 389-exception'),
                          ("389-exception with MIT",
                           'A license exception symbol can only be used as an exception in a "WITH exception" statement. for token: "389-exception". for license_expression: 389-exception WITH MIT'),
                          ])
def test_invalid_license_expression_with_invalid_exceptions(expression_string, expected_message):
    document: Document = document_fixture()
    license_expression: LicenseExpression = get_spdx_licensing().parse(expression_string)
    parent_id = "SPDXRef-File"
    context = ValidationContext(parent_id=parent_id, element_type=SpdxElementType.LICENSE_EXPRESSION,
                                full_element=license_expression)

    validation_messages: List[ValidationMessage] = validate_license_expression(license_expression, document, parent_id)
    expected_messages = [ValidationMessage(expected_message, context)]

    assert validation_messages == expected_messages
