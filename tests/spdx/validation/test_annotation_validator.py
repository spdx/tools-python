# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0

from typing import List

import pytest

from spdx_tools.spdx.model import Annotation, Document
from spdx_tools.spdx.validation.annotation_validator import validate_annotation
from spdx_tools.spdx.validation.validation_message import SpdxElementType, ValidationContext, ValidationMessage
from tests.spdx.fixtures import annotation_fixture, document_fixture, file_fixture


def test_valid_annotation():
    validation_messages: List[ValidationMessage] = validate_annotation(annotation_fixture(), document_fixture())

    assert validation_messages == []


@pytest.mark.parametrize(
    "annotation_id, file_id, expected_message",
    [
        (
            "SPDXRef-File",
            "SPDXRef-hiddenFile",
            'did not find the referenced spdx_id "SPDXRef-File" in the SPDX document',
        )
    ],
)
def test_invalid_annotation(annotation_id, file_id, expected_message):
    annotation: Annotation = annotation_fixture(spdx_id=annotation_id)
    document: Document = document_fixture(files=[file_fixture(spdx_id=file_id)])
    validation_messages: List[ValidationMessage] = validate_annotation(annotation, document)

    expected = ValidationMessage(
        expected_message, ValidationContext(element_type=SpdxElementType.ANNOTATION, full_element=annotation)
    )

    assert validation_messages == [expected]
