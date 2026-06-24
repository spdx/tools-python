# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from abc import abstractmethod
from dataclasses import field

from beartype.typing import List, Optional

from spdx_tools.common.typing.dataclass_with_properties import dataclass_with_properties
from spdx_tools.spdx3.model import Element


@dataclass_with_properties
class LicenseAddition(Element):
    addition_text: str = None
    is_deprecated_addition_id: Optional[bool] = None
    license_xml: Optional[str] = None
    obsoleted_by: Optional[str] = None
    see_also: List[str] = field(default_factory=list)
    standard_addition_template: Optional[str] = None

    @abstractmethod
    def __init__(self):
        pass
