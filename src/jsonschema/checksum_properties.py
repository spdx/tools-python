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

from src.jsonschema.json_property import JsonProperty
from src.model.checksum import Checksum, ChecksumAlgorithm
from src.writer.casing_tools import snake_case_to_camel_case


class ChecksumProperty(JsonProperty):
    ALGORITHM = auto()
    CHECKSUM_VALUE = auto()

    def json_property_name(self) -> str:
        return snake_case_to_camel_case(self.name)

    def get_property_value(self, checksum: Checksum) -> Any:
        if self == ChecksumProperty.ALGORITHM:
            return algorithm_to_json_string(checksum.algorithm)
        elif self == ChecksumProperty.CHECKSUM_VALUE:
            return checksum.value


def algorithm_to_json_string(algorithm: ChecksumAlgorithm) -> str:
    name_with_dash: str = algorithm.name.replace("_", "-")
    if "BLAKE2B" in name_with_dash:
        return name_with_dash.replace("BLAKE2B", "BLAKE2b")
    return name_with_dash
