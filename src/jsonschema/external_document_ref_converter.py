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
from typing import Type, Any

from src.jsonschema.checksum_converter import ChecksumConverter
from src.jsonschema.converter import TypedConverter
from src.jsonschema.external_document_ref_properties import ExternalDocumentRefProperty
from src.jsonschema.json_property import JsonProperty
from src.model.external_document_ref import ExternalDocumentRef
from src.writer.casing_tools import snake_case_to_camel_case


class ExternalDocumentRefConverter(TypedConverter):
    checksum_converter: ChecksumConverter

    def __init__(self):
        self.checksum_converter = ChecksumConverter()

    def json_property_name(self, property_thing: ExternalDocumentRefProperty) -> str:
        return snake_case_to_camel_case(property_thing.name)

    def get_property_value(self, external_document_ref: ExternalDocumentRef,
                           property_thing: ExternalDocumentRefProperty) -> Any:
        if property_thing == ExternalDocumentRefProperty.EXTERNAL_DOCUMENT_ID:
            return external_document_ref.document_ref_id
        elif property_thing == ExternalDocumentRefProperty.SPDX_DOCUMENT:
            return external_document_ref.document_uri
        elif property_thing == ExternalDocumentRefProperty.CHECKSUM:
            return self.checksum_converter.convert(external_document_ref.checksum)

    def get_json_type(self) -> Type[JsonProperty]:
        return ExternalDocumentRefProperty

    def get_data_model_type(self) -> Type[ExternalDocumentRef]:
        return ExternalDocumentRef
