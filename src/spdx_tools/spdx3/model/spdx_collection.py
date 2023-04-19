# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from abc import abstractmethod
from dataclasses import field
from typing import List, Optional

from spdx_tools.common.typing.dataclass_with_properties import dataclass_with_properties
from spdx_tools.spdx3.model.element import Element
from spdx_tools.spdx3.model.external_map import ExternalMap
from spdx_tools.spdx3.model.namespace_map import NamespaceMap


@dataclass_with_properties
class SpdxCollection(Element):
    # due to the inheritance we need to make all fields non-default in the __annotation__,
    # the __init__ method still raises an error if required fields are not set
    elements: List[str] = field(default_factory=list)
    root_elements: List[str] = field(default_factory=list)
    namespaces: Optional[List[NamespaceMap]] = field(default_factory=list)
    imports: Optional[List[ExternalMap]] = field(default_factory=list)

    @abstractmethod
    def __init__(self):
        pass
