# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from abc import ABC, abstractmethod

from beartype.typing import Optional

from spdx_tools.common.typing.dataclass_with_properties import dataclass_with_properties


@dataclass_with_properties
class IntegrityMethod(ABC):
    comment: Optional[str] = None

    @abstractmethod
    def __init__(self):
        pass
