from typing import Optional

from spdx_tools.common.typing.dataclass_with_properties import dataclass_with_properties
from spdx_tools.common.typing.type_checks import check_types_and_set_values


@dataclass_with_properties
class CdxPropertyEntry:
    cdx_prop_name: str = None
    cdx_prop_value: Optional[str] = None

    def __init__(self, cdx_prop_name: str, cdx_prop_value: Optional[str] = None):
        check_types_and_set_values(self, locals())
