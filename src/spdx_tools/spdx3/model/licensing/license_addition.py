# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from abc import ABC, abstractmethod
from dataclasses import field

from beartype.typing import List, Optional

from spdx_tools.common.typing.dataclass_with_properties import dataclass_with_properties


@dataclass_with_properties
class LicenseAddition(ABC):
    addition_id: str
    addition_name: str
    addition_text: str
    addition_comment: Optional[str] = None
    see_also: List[str] = field(default_factory=list)
    standard_addition_template: Optional[str] = None
    is_deprecated_addition_id: Optional[bool] = None
    obsoleted_by: Optional[str] = None

    @abstractmethod
    def __init__(self):
        pass
