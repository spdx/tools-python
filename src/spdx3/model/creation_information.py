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
from datetime import datetime
from typing import List

from semantic_version import Version

from common.typing.dataclass_with_properties import dataclass_with_properties
from common.typing.type_checks import check_types_and_set_values


@dataclass_with_properties
class CreationInformation:
    spec_version: Version
    created: datetime
    created_by: None  # placeholder for Actor
    profile: List[str]  # or create an Enum for ProfileIdentifier?
    data_license: str

    def __init__(self, spec_version: Version, created: datetime, created_by, profile: List[str],
                 data_license: str = "CC0"):
        check_types_and_set_values(self, locals())
