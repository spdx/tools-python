# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from beartype.typing import Dict

from spdx_tools.spdx3.model import Element


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
