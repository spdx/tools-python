# SPDX-FileCopyrightText: 2023 spdx contributors

# SPDX-License-Identifier: Apache-2.0
from abc import abstractmethod
from typing import Optional

from common.typing.dataclass_with_properties import dataclass_with_properties
from spdx3.model.element import Element


@dataclass_with_properties
class Artifact(Element):
    originated_by: Optional[str] = None  # SPDXID of the Agent/Tool

    @abstractmethod
    def __init__(self):
        pass
