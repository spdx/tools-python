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
from typing import Type, Any

from spdx.jsonschema.annotation_converter import AnnotationConverter
from spdx.jsonschema.checksum_converter import ChecksumConverter
from spdx.jsonschema.converter import TypedConverter
from spdx.jsonschema.file_properties import FileProperty
from spdx.jsonschema.json_property import JsonProperty
from spdx.jsonschema.optional_utils import apply_if_present
from spdx.model.document import Document
from spdx.model.file import File


class FileConverter(TypedConverter[File]):
    annotation_converter: AnnotationConverter
    checksum_converter: ChecksumConverter

    def __init__(self):
        self.annotation_converter = AnnotationConverter()
        self.checksum_converter = ChecksumConverter()

    def json_property_name(self, file_property: FileProperty) -> str:
        if file_property == FileProperty.SPDX_ID:
            return "SPDXID"
        return super().json_property_name(file_property)

    def _get_property_value(self, file: Any, file_property: FileProperty, document: Document = None) -> Any:
        if file_property == FileProperty.SPDX_ID:
            return file.spdx_id
        elif file_property == FileProperty.ANNOTATIONS:
            file_annotations = filter(lambda annotation: annotation.spdx_id == file.spdx_id, document.annotations)
            return [self.annotation_converter.convert(annotation) for annotation in file_annotations] or None
        elif file_property == FileProperty.ARTIFACT_OFS:
            # Deprecated property, automatically converted during parsing
            pass
        elif file_property == FileProperty.ATTRIBUTION_TEXTS:
            return file.attribution_texts or None
        elif file_property == FileProperty.CHECKSUMS:
            return [self.checksum_converter.convert(checksum) for checksum in file.checksums] or None
        elif file_property == FileProperty.COMMENT:
            return file.comment
        elif file_property == FileProperty.COPYRIGHT_TEXT:
            return apply_if_present(str, file.copyright_text)
        elif file_property == FileProperty.FILE_CONTRIBUTORS:
            return file.contributors or None
        elif file_property == FileProperty.FILE_DEPENDENCIES:
            # Deprecated property, automatically converted during parsing
            pass
        elif file_property == FileProperty.FILE_NAME:
            return file.name
        elif file_property == FileProperty.FILE_TYPES:
            return [file_type.name for file_type in file.file_types] or None
        elif file_property == FileProperty.LICENSE_COMMENTS:
            return file.license_comment
        elif file_property == FileProperty.LICENSE_CONCLUDED:
            return apply_if_present(str, file.license_concluded)
        elif file_property == FileProperty.LICENSE_INFO_IN_FILES:
            return [str(license_expression) for license_expression in file.license_info_in_file] or None
        elif file_property == FileProperty.NOTICE_TEXT:
            return file.notice

    def get_json_type(self) -> Type[JsonProperty]:
        return FileProperty

    def get_data_model_type(self) -> Type[File]:
        return File

    def requires_full_document(self) -> bool:
        return True
