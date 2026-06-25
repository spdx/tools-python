from dataclasses import field
from typing import List

from spdx_tools.common.typing.dataclass_with_properties import dataclass_with_properties
from spdx_tools.common.typing.type_checks import check_types_and_set_values
from spdx_tools.spdx3.model.extension.cdx_property_entry import CdxPropertyEntry
from spdx_tools.spdx3.model.extension.extension import Extension


@dataclass_with_properties
class CdxPropertiesExtension(Extension):
    cdx_property: List[CdxPropertyEntry] = field(default_factory=list)

    def __init__(self, cdx_property: List[CdxPropertyEntry] | None = None):
        cdx_property = [] if cdx_property is None else cdx_property
        check_types_and_set_values(self, locals())
