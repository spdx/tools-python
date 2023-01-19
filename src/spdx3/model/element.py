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
from abc import ABC, abstractmethod
from dataclasses import field
from typing import Optional, List

from common.typing.dataclass_with_properties import dataclass_with_properties

from spdx3.model.creation_information import CreationInformation
from spdx3.model.integrity_method import IntegrityMethod


@dataclass_with_properties
class Element(ABC):
    spdx_id: str  # IRI
    creation_info: CreationInformation
    name: Optional[str] = None
    summary: Optional[str] = None
    description: Optional[str] = None
    comment: Optional[str] = None
    verified_using: Optional[List[IntegrityMethod]] = field(default_factory=list)
    external_references: None = None  # placeholder for ExternalReference
    external_identifier: None = None  # placeholder for ExternalIdentifier
    extension: None = None  # placeholder for extension

    @abstractmethod
    def __init__(self):
        pass
