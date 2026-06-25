# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from abc import abstractmethod

from spdx_tools.common.typing.dataclass_with_properties import dataclass_with_properties
from spdx_tools.spdx3.model.element import Element


@dataclass_with_properties
class AnyLicenseInfo(Element):
    @abstractmethod
    def __init__(self):
        pass
