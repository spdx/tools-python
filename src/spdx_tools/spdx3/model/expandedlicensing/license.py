# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from abc import abstractmethod
from dataclasses import field

from beartype.typing import List, Optional

from spdx_tools.common.typing.dataclass_with_properties import dataclass_with_properties
from spdx_tools.spdx3.model.expandedlicensing.extendable_license import ExtendableLicense


@dataclass_with_properties
class License(ExtendableLicense):
    license_text: str = None
    see_also: List[str] = field(default_factory=list)
    is_osi_approved: Optional[bool] = None
    is_fsf_libre: Optional[bool] = None
    standard_license_header: Optional[str] = None
    standard_license_template: Optional[str] = None
    is_deprecated_license_id: Optional[bool] = None
    obsoleted_by: Optional[str] = None
    license_xml: Optional[str] = None

    @abstractmethod
    def __init__(self):
        pass
