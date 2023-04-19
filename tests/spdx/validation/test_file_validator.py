# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0

from typing import List
from unittest import TestCase

import pytest

from spdx_tools.spdx.model import Checksum, ChecksumAlgorithm
from spdx_tools.spdx.validation.file_validator import validate_file, validate_file_within_document
from spdx_tools.spdx.validation.validation_message import SpdxElementType, ValidationContext, ValidationMessage
from tests.spdx.fixtures import document_fixture, file_fixture


def test_valid_file():
    file = file_fixture()
    validation_messages: List[ValidationMessage] = validate_file_within_document(file, "SPDX-2.3", document_fixture())

    assert validation_messages == []


@pytest.mark.parametrize(
    "file_input, spdx_id, expected_message",
    [
        (
            file_fixture(name="/invalid/file/name"),
            file_fixture().spdx_id,
            'file name must not be an absolute path starting with "/", but is: /invalid/file/name',
        ),
        (
            file_fixture(checksums=[Checksum(ChecksumAlgorithm.MD2, "d4c41ce30a517d6ce9d79c8c17bb4b66")]),
            file_fixture().spdx_id,
            "checksums must contain a SHA1 algorithm checksum, but only contains: [<ChecksumAlgorithm.MD2: 13>]",
        ),
    ],
)
def test_invalid_file(file_input, spdx_id, expected_message):
    validation_messages: List[ValidationMessage] = validate_file_within_document(
        file_input, "SPDX-2.3", document_fixture()
    )

    expected = ValidationMessage(
        expected_message,
        ValidationContext(
            spdx_id=spdx_id,
            parent_id=document_fixture().creation_info.spdx_id,
            element_type=SpdxElementType.FILE,
            full_element=file_input,
        ),
    )

    assert validation_messages == [expected]


def test_v2_2mandatory_fields():
    file = file_fixture(license_concluded=None, license_info_in_file=[], copyright_text=None)

    assert validate_file(file, "SPDX-2.3") == []

    validation_messages: List[ValidationMessage] = validate_file(file, "SPDX-2.2")

    context = ValidationContext(spdx_id=file.spdx_id, element_type=SpdxElementType.FILE, full_element=file)
    mandatory_fields = ["license_concluded", "license_info_in_file", "copyright_text"]
    expected = [ValidationMessage(f"{field} is mandatory in SPDX-2.2", context) for field in mandatory_fields]

    TestCase().assertCountEqual(validation_messages, expected)
