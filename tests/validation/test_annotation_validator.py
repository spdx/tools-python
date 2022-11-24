from datetime import datetime
from typing import List

import pytest

from src.model.annotation import Annotation, AnnotationType
from src.model.document import Document
from src.validation.annotation_validator import AnnotationValidator
from src.validation.validation_message import ValidationMessage, ValidationContext, SpdxElementType
from tests.valid_defaults import get_actor, get_annotation, get_document, get_file


def test_correct_annotation():
    document: Document = get_document(files=[get_file(spdx_id="SPDXRef-File")])
    annotation_validator = AnnotationValidator("2.3", document)

    annotation = Annotation("SPDXRef-File", AnnotationType.OTHER, get_actor(), datetime(2022, 1, 1), "comment")
    validation_messages: List[ValidationMessage] = annotation_validator.validate_annotation(annotation)

    assert validation_messages == []


@pytest.mark.parametrize("annotation_id, file_id, expected_message",
                         [("SPDXRef-some_file", "SPDXRef-some_file",
                           'spdx_id must only contain letters, numbers, "." and "-" and must begin with "SPDXRef-", but is: SPDXRef-some_file'),
                          ("SPDXRef-File", "SPDXRef-hiddenFile",
                           'did not find the referenced spdx_id SPDXRef-File in the SPDX document')
                          ])
def test_wrong_annotation(annotation_id, file_id, expected_message):
    annotation: Annotation = get_annotation(spdx_id=annotation_id)
    document: Document = get_document(files=[get_file(spdx_id=file_id)])
    annotation_validator = AnnotationValidator("2.3", document)
    validation_messages: List[ValidationMessage] = annotation_validator.validate_annotation(annotation)

    expected = ValidationMessage(expected_message,
                                 ValidationContext(element_type=SpdxElementType.ANNOTATION,
                                                   full_element=annotation))

    assert validation_messages == [expected]
