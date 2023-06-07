# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from abc import abstractmethod
from dataclasses import field

from beartype.typing import List, Optional

from spdx_tools.common.typing.dataclass_with_properties import dataclass_with_properties
from spdx_tools.spdx3.model.licensing.any_license_info import AnyLicenseInfo


@dataclass_with_properties
class License(AnyLicenseInfo):
    license_id: str
    license_name: str
    license_text: str
    license_comment: Optional[str] = None
    see_also: List[str] = field(default_factory=list)
    is_osi_approved: Optional[bool] = None
    is_fsf_libre: Optional[bool] = None
    standard_license_header: Optional[str] = None
    standard_license_template: Optional[str] = None
    is_deprecated_license_id: Optional[bool] = None
    obsoleted_by: Optional[str] = None

    @abstractmethod
    def __init__(self):
        pass
