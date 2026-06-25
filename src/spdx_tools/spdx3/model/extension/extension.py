from abc import abstractmethod

from spdx_tools.common.typing.dataclass_with_properties import dataclass_with_properties


@dataclass_with_properties
class Extension:

    @abstractmethod
    def __init__(self):
        pass
