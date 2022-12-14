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

from src.datetime_conversions import datetime_to_iso_string
from src.jsonschema.json_property import JsonProperty
from src.model.document import CreationInfo
from src.writer.casing_tools import snake_case_to_camel_case


class CreationInfoProperty(JsonProperty):
    CREATED = auto()
    CREATORS = auto()
    LICENSE_LIST_VERSION = auto()
    COMMENT = auto()

    def json_property_name(self) -> str:
        return snake_case_to_camel_case(self.name)

    def get_property_value(self, creation_info: CreationInfo) -> Any:
        if self == CreationInfoProperty.CREATED:
            return datetime_to_iso_string(creation_info.created)
        elif self == CreationInfoProperty.CREATORS:
            return [creator.to_serialized_string() for creator in creation_info.creators]
        elif self == CreationInfoProperty.LICENSE_LIST_VERSION:
            return str(creation_info.license_list_version)
        elif self == CreationInfoProperty.COMMENT:
            return creation_info.creator_comment
