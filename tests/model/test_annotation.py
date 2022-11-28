from datetime import datetime

import pytest

from src.model.annotation import Annotation, AnnotationType


def test_correct_initialization():
    annotation = Annotation("id", AnnotationType.OTHER, "annotator", datetime(2022, 1, 1), "comment")
    assert annotation.spdx_id == "id"
    assert annotation.annotation_type == AnnotationType.OTHER
    assert annotation.annotator == "annotator"
    assert annotation.annotation_date == datetime(2022, 1, 1)
    assert annotation.annotation_comment == "comment"


def test_wrong_type_in_spdx_id():
    with pytest.raises(TypeError):
        Annotation(42, AnnotationType.OTHER, "annotator", datetime(2022, 1, 1), "comment")


def test_wrong_type_in_annotation_type():
    with pytest.raises(TypeError):
        Annotation("id", 42, "annotator", datetime(2022, 1, 1), "comment")


def test_wrong_type_in_annotator():
    with pytest.raises(TypeError):
        Annotation("id", AnnotationType.OTHER, 42, datetime(2022, 1, 1), "comment")


def test_wrong_type_in_annotation_date():
    with pytest.raises(TypeError):
        Annotation("id", AnnotationType.OTHER, "annotator", 42, "comment")


def test_wrong_type_in_annotation_comment():
    with pytest.raises(TypeError):
        Annotation("id", AnnotationType.OTHER, "annotator", datetime(2022, 1, 1), 42)
