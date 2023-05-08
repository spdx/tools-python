# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from abc import ABC, abstractmethod

from spdx_tools.common.typing.dataclass_with_properties import dataclass_with_properties
from spdx_tools.spdx3.model.licensing.license_field import LicenseField


@dataclass_with_properties
class AnyLicenseInfo(ABC, LicenseField):
    @abstractmethod
    def __init__(self):
        pass
