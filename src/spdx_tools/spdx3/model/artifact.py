# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from abc import abstractmethod
from dataclasses import field
from datetime import datetime

from beartype.typing import List, Optional

from spdx_tools.common.typing.dataclass_with_properties import dataclass_with_properties
from spdx_tools.spdx3.model import Element


@dataclass_with_properties
class Artifact(Element):
    originated_by: List[str] = field(default_factory=list)  # SPDXID of the Agent/Tool
    supplied_by: List[str] = field(default_factory=list)  # SPDXID of the Agent/Tool
    built_time: Optional[datetime] = None
    release_time: Optional[datetime] = None
    valid_until_time: Optional[datetime] = None
    standard: List[str] = field(default_factory=list)

    @abstractmethod
    def __init__(self):
        pass
