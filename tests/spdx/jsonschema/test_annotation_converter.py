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
from datetime import datetime

import pytest

from spdx.datetime_conversions import datetime_to_iso_string
from spdx.jsonschema.annotation_converter import AnnotationConverter
from spdx.jsonschema.annotation_properties import AnnotationProperty
from spdx.model.actor import Actor, ActorType
from spdx.model.annotation import Annotation, AnnotationType


@pytest.fixture
def converter() -> AnnotationConverter:
    return AnnotationConverter()


@pytest.mark.parametrize("annotation_property,expected", [(AnnotationProperty.ANNOTATION_DATE, "annotationDate"),
                                                          (AnnotationProperty.ANNOTATION_TYPE, "annotationType"),
                                                          (AnnotationProperty.ANNOTATOR, "annotator"),
                                                          (AnnotationProperty.COMMENT, "comment")])
def test_json_property_names(converter: AnnotationConverter, annotation_property: AnnotationProperty, expected: str):
    assert converter.json_property_name(annotation_property) == expected


def test_json_type(converter: AnnotationConverter):
    assert converter.get_json_type() == AnnotationProperty


def test_data_model_type(converter: AnnotationConverter):
    assert converter.get_data_model_type() == Annotation


def test_successful_conversion(converter: AnnotationConverter):
    date = datetime(2022, 12, 1)
    annotator = Actor(ActorType.PERSON, "actorName")
    annotation = Annotation("spdxId", AnnotationType.REVIEW, annotator,
                            date, "comment")

    converted_dict = converter.convert(annotation)

    assert converted_dict == {
        converter.json_property_name(AnnotationProperty.ANNOTATION_DATE): datetime_to_iso_string(date),
        converter.json_property_name(AnnotationProperty.ANNOTATION_TYPE): "REVIEW",
        converter.json_property_name(AnnotationProperty.ANNOTATOR): annotator.to_serialized_string(),
        converter.json_property_name(AnnotationProperty.COMMENT): "comment"
    }
