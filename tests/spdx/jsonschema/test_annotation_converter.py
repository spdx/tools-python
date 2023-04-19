# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from datetime import datetime

import pytest

from spdx_tools.spdx.datetime_conversions import datetime_to_iso_string
from spdx_tools.spdx.jsonschema.annotation_converter import AnnotationConverter
from spdx_tools.spdx.jsonschema.annotation_properties import AnnotationProperty
from spdx_tools.spdx.model import Actor, ActorType, Annotation, AnnotationType


@pytest.fixture
def converter() -> AnnotationConverter:
    return AnnotationConverter()


@pytest.mark.parametrize(
    "annotation_property,expected",
    [
        (AnnotationProperty.ANNOTATION_DATE, "annotationDate"),
        (AnnotationProperty.ANNOTATION_TYPE, "annotationType"),
        (AnnotationProperty.ANNOTATOR, "annotator"),
        (AnnotationProperty.COMMENT, "comment"),
    ],
)
def test_json_property_names(converter: AnnotationConverter, annotation_property: AnnotationProperty, expected: str):
    assert converter.json_property_name(annotation_property) == expected


def test_json_type(converter: AnnotationConverter):
    assert converter.get_json_type() == AnnotationProperty


def test_data_model_type(converter: AnnotationConverter):
    assert converter.get_data_model_type() == Annotation


def test_successful_conversion(converter: AnnotationConverter):
    date = datetime(2022, 12, 1)
    annotator = Actor(ActorType.PERSON, "actorName")
    annotation = Annotation("spdxId", AnnotationType.REVIEW, annotator, date, "comment")

    converted_dict = converter.convert(annotation)

    assert converted_dict == {
        converter.json_property_name(AnnotationProperty.ANNOTATION_DATE): datetime_to_iso_string(date),
        converter.json_property_name(AnnotationProperty.ANNOTATION_TYPE): "REVIEW",
        converter.json_property_name(AnnotationProperty.ANNOTATOR): annotator.to_serialized_string(),
        converter.json_property_name(AnnotationProperty.COMMENT): "comment",
    }
