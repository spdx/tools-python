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
from enum import Enum, auto
from typing import Optional

from common.typing.dataclass_with_properties import dataclass_with_properties
from common.typing.type_checks import check_types_and_set_values


class ExternalIdentifierType(Enum):
    CPE22 = auto()
    CPE23 = auto()
    GITOID = auto()
    OTHER = auto()
    PKG_URL = auto()
    SWHID = auto()
    SWID = auto()


@dataclass_with_properties
class ExternalIdentifier:
    external_identifier_type: ExternalIdentifierType
    identifier: str
    comment: Optional[str] = None

    def __init__(self, external_identifier_type: ExternalIdentifierType, identifier: str,
                 comment: Optional[str] = None):
        check_types_and_set_values(self, locals())
