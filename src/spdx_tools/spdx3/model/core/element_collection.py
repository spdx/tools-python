# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from abc import abstractmethod
from dataclasses import field

from beartype.typing import List

from spdx_tools.common.typing.dataclass_with_properties import dataclass_with_properties

from .element import Element
from .external_map import ExternalMap
from .namespace_map import NamespaceMap


@dataclass_with_properties
class ElementCollection(Element):
    # due to the inheritance we need to make all fields non-default in the __annotation__,
    # the __init__ method still raises an error if required fields are not set
    element: List[str] = field(default_factory=list)
    root_element: List[str] = field(default_factory=list)
    namespace: List[NamespaceMap] = field(default_factory=list)
    import_: List[ExternalMap] = field(default_factory=list)

    @abstractmethod
    def __init__(self):
        pass
