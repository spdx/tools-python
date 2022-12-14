#  Copyright (c) 2022 spdx contributors
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#      http://www.apache.org/licenses/LICENSE-2.0
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
from enum import auto
from typing import Any

from src.jsonschema.checksum_properties import ChecksumProperty
from src.jsonschema.common_conversions import convert_complex_type
from src.jsonschema.json_property import JsonProperty
from src.model.external_document_ref import ExternalDocumentRef
from src.writer.casing_tools import snake_case_to_camel_case


class ExternalDocumentRefProperty(JsonProperty):
    EXTERNAL_DOCUMENT_ID = auto()
    SPDX_DOCUMENT = auto()
    CHECKSUM = auto()

    def json_property_name(self) -> str:
        return snake_case_to_camel_case(self.name)

    def get_property_value(self, external_document_ref: ExternalDocumentRef) -> Any:
        if self == ExternalDocumentRefProperty.EXTERNAL_DOCUMENT_ID:
            return external_document_ref.document_ref_id
        elif self == ExternalDocumentRefProperty.SPDX_DOCUMENT:
            return external_document_ref.document_uri
        elif self == ExternalDocumentRefProperty.CHECKSUM:
            return convert_complex_type(external_document_ref.checksum, ChecksumProperty)
