# Copyright (c) 2023 spdx contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from typing import Dict

from spdx3.model.element import Element


class Payload:
    _spdx_id_map: Dict[str, Element]

    def __init__(self, spdx_id_map: Dict[str, Element] = None):
        self._spdx_id_map = spdx_id_map if spdx_id_map else {}

    def add_element(self, element: Element):
        self._spdx_id_map[element.spdx_id] = element

    def get_element(self, spdx_id: str) -> Element:
        return self._spdx_id_map[spdx_id]

    def get_full_map(self) -> Dict[str, Element]:
        return self._spdx_id_map
