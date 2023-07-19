# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0

from typing import List
from unittest import TestCase

import pytest
from license_expression import Licensing

from spdx_tools.spdx.constants import DOCUMENT_SPDX_ID
from spdx_tools.spdx.model import Relationship, RelationshipType, SpdxNoAssertion, SpdxNone
from spdx_tools.spdx.validation.package_validator import validate_package, validate_package_within_document
from spdx_tools.spdx.validation.validation_message import SpdxElementType, ValidationContext, ValidationMessage
from tests.spdx.fixtures import document_fixture, file_fixture, package_fixture, package_verification_code_fixture


def test_valid_package():
    package = package_fixture()
    validation_messages: List[ValidationMessage] = validate_package_within_document(
        package, "SPDX-2.3", document_fixture()
    )

    assert validation_messages == []


@pytest.mark.parametrize(
    "package_input, expected_message",
    [
        (
            package_fixture(
                files_analyzed=False, verification_code=package_verification_code_fixture(), license_info_from_files=[]
            ),
            f"verification_code must be None if files_analyzed is False, but is: "
            f"{package_verification_code_fixture()}",
        ),
        (
            package_fixture(files_analyzed=False, license_info_from_files=[SpdxNone()], verification_code=None),
            "license_info_from_files must be None if files_analyzed is False, but is: [NONE]",
        ),
        (
            package_fixture(files_analyzed=False, license_info_from_files=[SpdxNoAssertion()], verification_code=None),
            "license_info_from_files must be None if files_analyzed is False, but is: [NOASSERTION]",
        ),
        (
            package_fixture(
                files_analyzed=False,
                license_info_from_files=[Licensing().parse("some_license")],
                verification_code=None,
            ),
            "license_info_from_files must be None if files_analyzed is False, but is: [LicenseSymbol('some_license', "
            "is_exception=False)]",
        ),
    ],
)
def test_invalid_package(package_input, expected_message):
    validation_messages: List[ValidationMessage] = validate_package_within_document(
        package_input, "SPDX-2.3", document_fixture(relationships=[])
    )

    expected = ValidationMessage(
        expected_message,
        ValidationContext(
            spdx_id=package_input.spdx_id,
            parent_id=DOCUMENT_SPDX_ID,
            element_type=SpdxElementType.PACKAGE,
            full_element=package_input,
        ),
    )

    assert validation_messages == [expected]


@pytest.mark.parametrize(
    "relationships",
    [
        [Relationship("SPDXRef-Package", RelationshipType.CONTAINS, "DocumentRef-external:SPDXRef-File")],
        [Relationship("DocumentRef-external:SPDXRef-File", RelationshipType.CONTAINED_BY, "SPDXRef-Package")],
    ],
)
def test_valid_package_with_contains(relationships):
    document = document_fixture(
        relationships=relationships,
        files=[file_fixture(spdx_id="SPDXRef-File1"), file_fixture(spdx_id="SPDXRef-File2")],
    )
    package = package_fixture(files_analyzed=False, verification_code=None, license_info_from_files=[])

    validation_messages: List[ValidationMessage] = validate_package_within_document(package, "SPDX-2.3", document)

    assert validation_messages == []


@pytest.mark.parametrize(
    "relationships",
    [
        [Relationship("SPDXRef-Package", RelationshipType.CONTAINS, "SPDXRef-File1")],
        [Relationship("SPDXRef-File2", RelationshipType.CONTAINED_BY, "SPDXRef-Package")],
        [
            Relationship("SPDXRef-Package", RelationshipType.CONTAINS, "SPDXRef-File2"),
            Relationship("SPDXRef-File1", RelationshipType.CONTAINED_BY, "SPDXRef-Package"),
        ],
    ],
)
def test_invalid_package_with_contains(relationships):
    document = document_fixture(
        relationships=relationships,
        files=[file_fixture(spdx_id="SPDXRef-File1"), file_fixture(spdx_id="SPDXRef-File2")],
    )
    package = package_fixture(files_analyzed=False, verification_code=None, license_info_from_files=[])
    context = ValidationContext(
        spdx_id=package.spdx_id,
        parent_id=document.creation_info.spdx_id,
        element_type=SpdxElementType.PACKAGE,
        full_element=package,
    )

    validation_messages: List[ValidationMessage] = validate_package_within_document(package, "SPDX-2.3", document)

    assert validation_messages == [
        ValidationMessage(
            f"package must contain no elements if files_analyzed is False, but found {relationships}", context
        )
    ]


def test_v2_3only_fields():
    package = package_fixture()
    validation_messages: List[ValidationMessage] = validate_package(package, "SPDX-2.2")

    context = ValidationContext(spdx_id=package.spdx_id, element_type=SpdxElementType.PACKAGE, full_element=package)
    unsupported_fields = ["primary_package_purpose", "built_date", "release_date", "valid_until_date"]
    expected = [ValidationMessage(f"{field} is not supported in SPDX-2.2", context) for field in unsupported_fields]

    TestCase().assertCountEqual(validation_messages, expected)


def test_v2_2mandatory_fields():
    package = package_fixture(
        license_concluded=None,
        license_declared=None,
        copyright_text=None,
        primary_package_purpose=None,
        built_date=None,
        release_date=None,
        valid_until_date=None,
    )

    assert validate_package(package, "SPDX-2.3") == []

    validation_messages: List[ValidationMessage] = validate_package(package, "SPDX-2.2")

    context = ValidationContext(spdx_id=package.spdx_id, element_type=SpdxElementType.PACKAGE, full_element=package)
    mandatory_fields = ["license_concluded", "license_declared", "copyright_text"]
    expected = [ValidationMessage(f"{field} is mandatory in SPDX-2.2", context) for field in mandatory_fields]

    TestCase().assertCountEqual(validation_messages, expected)
