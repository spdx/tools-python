from datetime import datetime
from typing import List

from src.model.annotation import Annotation, AnnotationType
from src.validation.annotation_validator import AnnotationValidator
from src.validation.validation_message import ValidationMessage, ValidationContext, SpdxElementType
from tests.valid_defaults import get_actor


def test_correct_annotation():
    annotation_validator = AnnotationValidator("2.3")

    annotation = Annotation("id", AnnotationType.OTHER, get_actor(), datetime(2022, 1, 1), "comment")
    validation_messages: List[ValidationMessage] = annotation_validator.validate_annotation(annotation)

    assert validation_messages == []
