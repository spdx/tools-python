# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from beartype.typing import Any, Type

from spdx_tools.spdx.datetime_conversions import datetime_to_iso_string
from spdx_tools.spdx.jsonschema.annotation_properties import AnnotationProperty
from spdx_tools.spdx.jsonschema.converter import TypedConverter
from spdx_tools.spdx.jsonschema.json_property import JsonProperty
from spdx_tools.spdx.model import Annotation, Document


class AnnotationConverter(TypedConverter[Annotation]):
    def _get_property_value(
        self, annotation: Annotation, annotation_property: AnnotationProperty, document: Document = None
    ) -> Any:
        if annotation_property == AnnotationProperty.ANNOTATION_DATE:
            return datetime_to_iso_string(annotation.annotation_date)
        elif annotation_property == AnnotationProperty.ANNOTATION_TYPE:
            return annotation.annotation_type.name
        elif annotation_property == AnnotationProperty.ANNOTATOR:
            return annotation.annotator.to_serialized_string()
        elif annotation_property == AnnotationProperty.COMMENT:
            return annotation.annotation_comment

    def get_json_type(self) -> Type[JsonProperty]:
        return AnnotationProperty

    def get_data_model_type(self) -> Type[Annotation]:
        return Annotation
