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
from typing import Type, Any, Tuple, Dict

from spdx.jsonschema.annotation_converter import AnnotationConverter
from spdx.jsonschema.converter import TypedConverter
from spdx.jsonschema.json_property import JsonProperty
from spdx.jsonschema.optional_utils import apply_if_present
from spdx.jsonschema.snippet_properties import SnippetProperty
from spdx.model.document import Document
from spdx.model.snippet import Snippet


class SnippetConverter(TypedConverter[Snippet]):
    annotation_converter: AnnotationConverter

    def __init__(self):
        self.annotation_converter = AnnotationConverter()

    def json_property_name(self, snippet_property: SnippetProperty) -> str:
        if snippet_property == SnippetProperty.SPDX_ID:
            return "SPDXID"
        return super().json_property_name(snippet_property)

    def _get_property_value(self, snippet: Snippet, snippet_property: SnippetProperty,
                            document: Document = None) -> Any:
        if snippet_property == SnippetProperty.SPDX_ID:
            return snippet.spdx_id
        elif snippet_property == SnippetProperty.ANNOTATIONS:
            snippet_annotations = filter(lambda annotation: annotation.spdx_id == snippet.spdx_id, document.annotations)
            return [self.annotation_converter.convert(annotation) for annotation in snippet_annotations] or None
        elif snippet_property == SnippetProperty.ATTRIBUTION_TEXTS:
            return snippet.attribution_texts or None
        elif snippet_property == SnippetProperty.COMMENT:
            return snippet.comment
        elif snippet_property == SnippetProperty.COPYRIGHT_TEXT:
            return apply_if_present(str, snippet.copyright_text)
        elif snippet_property == SnippetProperty.LICENSE_COMMENTS:
            return snippet.license_comment
        elif snippet_property == SnippetProperty.LICENSE_CONCLUDED:
            return apply_if_present(str, snippet.license_concluded)
        elif snippet_property == SnippetProperty.LICENSE_INFO_IN_SNIPPETS:
            return [str(license_expression) for license_expression in snippet.license_info_in_snippet] or None
        elif snippet_property == SnippetProperty.NAME:
            return snippet.name
        elif snippet_property == SnippetProperty.RANGES:
            ranges = [convert_byte_range_to_dict(snippet.byte_range, snippet.file_spdx_id)]
            if snippet.line_range:
                ranges.append(convert_line_range_to_dict(snippet.line_range, snippet.file_spdx_id))
            return ranges
        elif snippet_property == SnippetProperty.SNIPPET_FROM_FILE:
            return snippet.file_spdx_id

    def get_json_type(self) -> Type[JsonProperty]:
        return SnippetProperty

    def get_data_model_type(self) -> Type[Snippet]:
        return Snippet

    def requires_full_document(self) -> bool:
        return True


def convert_line_range_to_dict(line_range: Tuple[int, int], file_id: str) -> Dict:
    return _convert_range_to_dict(line_range, file_id, "lineNumber")


def convert_byte_range_to_dict(byte_range: Tuple[int, int], file_id: str) -> Dict:
    return _convert_range_to_dict(byte_range, file_id, "offset")


def _convert_range_to_dict(int_range: Tuple[int, int], file_id: str, pointer_property: str) -> Dict:
    return {"startPointer": _pointer(file_id, int_range[0], pointer_property),
            "endPointer": _pointer(file_id, int_range[1], pointer_property)}


def _pointer(reference: str, target: int, pointer_property: str) -> Dict:
    return {"reference": reference, pointer_property: target}
