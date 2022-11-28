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
from typing import Dict, Optional, List, Union

from src.parser.json.snippet_parser import RangeType


def set_optional_property(property_name: Union[str, RangeType], parse_object: Dict) -> Optional[str, int, Dict, List, bool]:
    if property_name in parse_object:
        property_value = parse_object.get(property_name)
        return property_value
    else:
        return None
