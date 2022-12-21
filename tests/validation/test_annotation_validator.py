from datetime import datetime
from typing import List

import pytest

from src.model.annotation import Annotation, AnnotationType
from src.model.document import Document
from src.validation.annotation_validator import validate_annotation
from src.validation.validation_message import ValidationMessage, ValidationContext, SpdxElementType
from tests.valid_defaults import get_actor, get_annotation, get_document, get_file


def test_valid_annotation():
    document: Document = get_document(files=[get_file(spdx_id="SPDXRef-File")])

    annotation = Annotation("SPDXRef-File", AnnotationType.OTHER, get_actor(), datetime(2022, 1, 1), "comment")
    validation_messages: List[ValidationMessage] = validate_annotation(annotation, document)

    assert validation_messages == []


@pytest.mark.parametrize("annotation_id, file_id, expected_message",
                         [("SPDXRef-File", "SPDXRef-hiddenFile",
                           "did not find the referenced spdx_id SPDXRef-File in the SPDX document")
                          ])
def test_invalid_annotation(annotation_id, file_id, expected_message):
    annotation: Annotation = get_annotation(spdx_id=annotation_id)
    document: Document = get_document(files=[get_file(spdx_id=file_id)])
    validation_messages: List[ValidationMessage] = validate_annotation(annotation, document)

    expected = ValidationMessage(expected_message,
                                 ValidationContext(element_type=SpdxElementType.ANNOTATION,
                                                   full_element=annotation))

    assert validation_messages == [expected]
