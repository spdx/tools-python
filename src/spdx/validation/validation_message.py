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

from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional, Any


class SpdxElementType(Enum):
    LICENSE_EXPRESSION = auto()
    PACKAGE_VERIFICATION_CODE = auto()
    EXTERNAL_DOCUMENT_REF = auto()
    CHECKSUM = auto()
    EXTERNAL_PACKAGE_REF = auto()
    ACTOR = auto()
    DOCUMENT = auto()
    CREATION_INFO = auto()
    PACKAGE = auto()
    FILE = auto()
    SNIPPET = auto()
    ANNOTATION = auto()
    RELATIONSHIP = auto()
    EXTRACTED_LICENSING_INFO = auto()


@dataclass(frozen=True)
class ValidationContext:
    spdx_id: Optional[str] = None  # not every type has an id, or it might be missing
    parent_id: Optional[str] = None  # if a parent is known and has a valid id
    element_type: Optional[SpdxElementType] = None
    full_element: Any = None  # can be any class of the data model


@dataclass(frozen=True)
class ValidationMessage:
    validation_message: str
    context: ValidationContext
