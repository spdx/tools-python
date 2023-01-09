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

from spdx.datetime_conversions import datetime_to_iso_string
from spdx.jsonschema.converter import TypedConverter
from spdx.jsonschema.creation_info_properties import CreationInfoProperty
from spdx.jsonschema.json_property import JsonProperty
from spdx.jsonschema.optional_utils import apply_if_present
from spdx.model.document import CreationInfo, Document


class CreationInfoConverter(TypedConverter[CreationInfo]):
    def get_data_model_type(self) -> Type[CreationInfo]:
        return CreationInfo

    def get_json_type(self) -> Type[JsonProperty]:
        return CreationInfoProperty

    def _get_property_value(self, creation_info: CreationInfo, creation_info_property: CreationInfoProperty,
                            _document: Document = None) -> Any:
        if creation_info_property == CreationInfoProperty.CREATED:
            return datetime_to_iso_string(creation_info.created)
        elif creation_info_property == CreationInfoProperty.CREATORS:
            return [creator.to_serialized_string() for creator in creation_info.creators] or None
        elif creation_info_property == CreationInfoProperty.LICENSE_LIST_VERSION:
            return apply_if_present(str, creation_info.license_list_version)
        elif creation_info_property == CreationInfoProperty.COMMENT:
            return creation_info.creator_comment
