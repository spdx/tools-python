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
from enum import Enum, auto
from typing import Optional, List

from common.typing.dataclass_with_properties import dataclass_with_properties
from common.typing.type_checks import check_types_and_set_values


class ExternalReferenceType(Enum):
    ALT_DOWNLOAD_LOCATION = auto()
    ALT_WEB_PAGE = auto()
    OTHER = auto()
    SECURITY_ADVISORY = auto()
    SECURITY_FIX = auto()
    SECURITY_OTHER = auto()


@dataclass_with_properties
class ExternalReference:
    external_reference_type: Optional[ExternalReferenceType] = None
    locator: List[str] = field(default_factory=list)
    content_type: Optional[str] = None  # placeholder for MediaType
    comment: Optional[str] = None

    def __init__(self, external_reference_type: Optional[ExternalReferenceType] = None, locator: List[str] = None,
                 content_type: Optional[str] = None, comment: Optional[str] = None):
        locator = [] if locator is None else locator
        check_types_and_set_values(self, locals())
