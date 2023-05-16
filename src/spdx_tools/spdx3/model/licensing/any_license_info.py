# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from abc import abstractmethod

from spdx_tools.spdx3.model.licensing.license_field import LicenseField


class AnyLicenseInfo(LicenseField):
    @abstractmethod
    def __init__(self):
        pass
