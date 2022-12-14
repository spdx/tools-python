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
from enum import auto
from typing import Any

from src.jsonschema.common_conversions import convert_complex_type
from src.jsonschema.external_document_ref_properties import ExternalDocumentRefProperty
from src.jsonschema.json_property import JsonProperty
from src.model.document import CreationInfo
from src.writer.casing_tools import snake_case_to_camel_case


class DocumentProperty(JsonProperty):
    SPDX_VERSION = auto()
    SPDX_ID = auto()
    NAME = auto()
    DOCUMENT_NAMESPACE = auto()
    DATA_LICENSE = auto()
    EXTERNAL_DOCUMENT_REFS = auto()
    COMMENT = auto()

    def json_property_name(self) -> str:
        if self == DocumentProperty.SPDX_ID:
            return "SPDXID"
        return snake_case_to_camel_case(self.name)

    def get_property_value(self, creation_info: CreationInfo) -> Any:
        if self == DocumentProperty.SPDX_VERSION:
            return creation_info.spdx_version
        elif self == DocumentProperty.SPDX_ID:
            return creation_info.spdx_id
        elif self == DocumentProperty.NAME:
            return creation_info.name
        elif self == DocumentProperty.DATA_LICENSE:
            return creation_info.data_license
        elif self == DocumentProperty.EXTERNAL_DOCUMENT_REFS:
            return [convert_complex_type(external_document_ref, ExternalDocumentRefProperty) for external_document_ref
                    in creation_info.external_document_refs]
        elif self == DocumentProperty.COMMENT:
            return creation_info.document_comment
