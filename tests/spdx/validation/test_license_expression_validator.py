# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0

from typing import List
from unittest import TestCase

import pytest
from license_expression import LicenseExpression

from spdx_tools.common.spdx_licensing import spdx_licensing
from spdx_tools.spdx.model import Document, SpdxNoAssertion, SpdxNone
from spdx_tools.spdx.validation.license_expression_validator import (
    validate_license_expression,
    validate_license_expressions,
)
from spdx_tools.spdx.validation.validation_message import SpdxElementType, ValidationContext, ValidationMessage
from tests.spdx.fixtures import document_fixture, external_document_ref_fixture, extracted_licensing_info_fixture

FIXTURE_LICENSE_ID = extracted_licensing_info_fixture().license_id
EXTERNAL_DOCUMENT_ID = external_document_ref_fixture().document_ref_id


@pytest.mark.parametrize(
    "expression_string",
    [
        "MIT",
        FIXTURE_LICENSE_ID,
        f"GPL-2.0-only with GPL-CC-1.0 and {FIXTURE_LICENSE_ID} with 389-exception or Beerware",
        f"{EXTERNAL_DOCUMENT_ID}:LicenseRef-007",
    ],
)
def test_valid_license_expression(expression_string):
    document: Document = document_fixture()
    license_expression: LicenseExpression = spdx_licensing.parse(expression_string)
    validation_messages: List[ValidationMessage] = validate_license_expression(
        license_expression, document, parent_id="SPDXRef-File"
    )

    assert validation_messages == []


@pytest.mark.parametrize("expression", [SpdxNone(), SpdxNoAssertion()])
def test_none_and_no_assertion(expression):
    document: Document = document_fixture()
    validation_messages: List[ValidationMessage] = validate_license_expression(
        expression, document, parent_id="SPDXRef-File"
    )
    assert validation_messages == []


@pytest.mark.parametrize(
    "expression_list",
    [
        [SpdxNone()],
        [SpdxNoAssertion()],
        [spdx_licensing.parse("MIT and GPL-3.0-only"), spdx_licensing.parse(FIXTURE_LICENSE_ID)],
        [SpdxNone(), spdx_licensing.parse("MIT"), SpdxNoAssertion()],
    ],
)
def test_valid_license_expressions(expression_list):
    document: Document = document_fixture()
    validation_messages: List[ValidationMessage] = validate_license_expressions(
        expression_list, document, parent_id="SPDXRef-File"
    )
    assert validation_messages == []


@pytest.mark.parametrize(
    "expression_string, unknown_symbols",
    [
        (f"{FIXTURE_LICENSE_ID} or LicenseRef-22", ["LicenseRef-22"]),
        ("nope with 389-exception and _.- or LicenseRef-10", ["nope", "_.-", "LicenseRef-10"]),
    ],
)
def test_invalid_license_expression_with_unknown_symbols(expression_string, unknown_symbols):
    document: Document = document_fixture()
    license_expression: LicenseExpression = spdx_licensing.parse(expression_string)
    parent_id = "SPDXRef-File"
    context = ValidationContext(
        parent_id=parent_id, element_type=SpdxElementType.LICENSE_EXPRESSION, full_element=license_expression
    )

    validation_messages: List[ValidationMessage] = validate_license_expression(license_expression, document, parent_id)
    expected_messages = [
        ValidationMessage(
            f"Unrecognized license reference: {symbol}. license_expression must only use IDs from the license list or "
            f"extracted licensing info, but is: {license_expression}",
            context,
        )
        for symbol in unknown_symbols
    ]

    TestCase().assertCountEqual(validation_messages, expected_messages)


@pytest.mark.parametrize(
    "expression_string, expected_message",
    [
        (
            "MIT with MIT",
            'A plain license symbol cannot be used as an exception in a "WITH symbol" statement. for token: "MIT" at '
            "position: 9. for license_expression: MIT WITH MIT",
        ),
        (
            f"GPL-2.0-or-later and {FIXTURE_LICENSE_ID} with {FIXTURE_LICENSE_ID}",
            f'A plain license symbol cannot be used as an exception in a "WITH symbol" statement. for token: '
            f'"{FIXTURE_LICENSE_ID}" at position: 39. for license_expression: GPL-2.0-or-later AND '
            f"{FIXTURE_LICENSE_ID} WITH {FIXTURE_LICENSE_ID}",
        ),
        (
            f"GPL-2.0-or-later with MIT and {FIXTURE_LICENSE_ID} with GPL-2.0-or-later",
            f'A plain license symbol cannot be used as an exception in a "WITH symbol" statement. for token: "MIT" at '
            f"position: 22. for license_expression: GPL-2.0-or-later WITH MIT AND {FIXTURE_LICENSE_ID} "
            f"WITH GPL-2.0-or-later",
        ),
        (
            "389-exception with 389-exception",
            'A license exception symbol can only be used as an exception in a "WITH exception" statement. for token: '
            '"389-exception". for license_expression: 389-exception WITH 389-exception',
        ),
        (
            "389-exception with MIT",
            'A license exception symbol can only be used as an exception in a "WITH exception" statement. for token: '
            '"389-exception". for license_expression: 389-exception WITH MIT',
        ),
    ],
)
def test_invalid_license_expression_with_invalid_exceptions(expression_string, expected_message):
    document: Document = document_fixture()
    license_expression: LicenseExpression = spdx_licensing.parse(expression_string)
    parent_id = "SPDXRef-File"
    context = ValidationContext(
        parent_id=parent_id, element_type=SpdxElementType.LICENSE_EXPRESSION, full_element=license_expression
    )

    validation_messages: List[ValidationMessage] = validate_license_expression(license_expression, document, parent_id)
    expected_messages = [ValidationMessage(expected_message, context)]

    assert validation_messages == expected_messages


@pytest.mark.parametrize(
    "expression_string, expected_message",
    [
        (
            f"{EXTERNAL_DOCUMENT_ID}:LicenseRef-007:4",
            f"Too many colons in license reference: {EXTERNAL_DOCUMENT_ID}:LicenseRef-007:4. "
            "A license reference must only contain a single colon to "
            "separate an external document reference from the license reference.",
        ),
        (
            f"{EXTERNAL_DOCUMENT_ID}:unknown_license",
            'A license reference must start with "LicenseRef-", but is: unknown_license '
            f"in external license reference {EXTERNAL_DOCUMENT_ID}:unknown_license.",
        ),
        (
            "DocumentRef-unknown:LicenseRef-1",
            'Did not find the external document reference "DocumentRef-unknown" in the SPDX document. '
            "From the external license reference DocumentRef-unknown:LicenseRef-1.",
        ),
    ],
)
def test_invalid_license_expression_with_external_reference(expression_string, expected_message):
    document: Document = document_fixture()
    license_expression: LicenseExpression = spdx_licensing.parse(expression_string)
    parent_id = "SPDXRef-File"
    context = ValidationContext(
        parent_id=parent_id, element_type=SpdxElementType.LICENSE_EXPRESSION, full_element=license_expression
    )

    validation_messages: List[ValidationMessage] = validate_license_expression(license_expression, document, parent_id)
    expected_messages = [ValidationMessage(expected_message, context)]

    assert validation_messages == expected_messages
