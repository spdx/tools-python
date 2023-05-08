# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

from spdx_tools.common.typing.dataclass_with_properties import dataclass_with_properties
from spdx_tools.spdx3.model import Agent, Element, Relationship


@dataclass_with_properties
class VulnAssessmentRelationship(Relationship, ABC):
    assessed_element: Optional[Element] = None
    published_time: Optional[datetime] = None
    supplied_by: Optional[Agent] = None
    modified_time: Optional[datetime] = None
    withdrawn_time: Optional[datetime] = None

    @abstractmethod
    def __init__(self):
        pass
