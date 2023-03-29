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

from spdx.jsonschema.json_property import JsonProperty


class RelationshipProperty(JsonProperty):
    SPDX_ELEMENT_ID = auto()
    COMMENT = auto()
    RELATED_SPDX_ELEMENT = auto()
    RELATIONSHIP_TYPE = auto()
