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

from src.datetime_conversions import datetime_to_iso_string
from src.jsonschema.converter import TypedConverter
from src.jsonschema.creation_info_properties import CreationInfoProperty
from src.jsonschema.json_property import JsonProperty
from src.jsonschema.optional_utils import apply_if_present
from src.model.document import CreationInfo, Document
from src.writer.casing_tools import snake_case_to_camel_case


class CreationInfoConverter(TypedConverter):
    def get_data_model_type(self) -> Type[CreationInfo]:
        return CreationInfo

    def get_json_type(self) -> Type[JsonProperty]:
        return CreationInfoProperty

    def json_property_name(self, creation_info_property: CreationInfoProperty) -> str:
        return snake_case_to_camel_case(creation_info_property.name)

    def _get_property_value(self, creation_info: CreationInfo, creation_info_property: CreationInfoProperty,
                            _document: Document = None) -> Any:
        if creation_info_property == CreationInfoProperty.CREATED:
            return datetime_to_iso_string(creation_info.created)
        elif creation_info_property == CreationInfoProperty.CREATORS:
            return [creator.to_serialized_string() for creator in creation_info.creators]
        elif creation_info_property == CreationInfoProperty.LICENSE_LIST_VERSION:
            return apply_if_present(str, creation_info.license_list_version)
        elif creation_info_property == CreationInfoProperty.COMMENT:
            return creation_info.creator_comment
