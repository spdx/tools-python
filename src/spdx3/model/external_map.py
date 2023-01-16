# Copyright (c) 2023 spdx contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#   http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from dataclasses import field
from typing import Optional, List
from common.typing.type_checks import check_types_and_set_values

from common.typing.dataclass_with_properties import dataclass_with_properties
from spdx3.model.integrity_method import IntegrityMethod


@dataclass_with_properties
class ExternalMap:
    external_id: str  # anyURI
    verified_using: Optional[List[IntegrityMethod]] = field(default_factory=list)
    location_hint: Optional[str] = None  # anyURI

    def __init__(self, external_id: str, verified_using: Optional[List[IntegrityMethod]]= None, location_hint: Optional[str] = None):
        verified_using = [] if verified_using is None else verified_using
        check_types_and_set_values(self, locals())
