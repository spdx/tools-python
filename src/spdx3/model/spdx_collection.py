# Copyright (c) 2023 spdx contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#    http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from abc import abstractmethod
from dataclasses import field
from typing import List, Optional

from common.typing.dataclass_with_properties import dataclass_with_properties

from spdx3.model.element import Element
from spdx3.model.external_map import ExternalMap
from spdx3.model.namespace_map import NamespaceMap


@dataclass_with_properties
class SpdxCollection(Element):
    # due to the inheritance we need to make all fields non-default in the __annotation__, the __init__ method still raises an error if required fields are not set
    elements: List[str] = field(default_factory=list)
    root_elements: List[str] = field(default_factory=list)
    namespaces: Optional[List[NamespaceMap]] = field(default_factory=list)
    imports: Optional[List[ExternalMap]] = field(default_factory=list)

    @abstractmethod
    def __init__(self):
        pass
