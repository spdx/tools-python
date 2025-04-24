# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from .license_field import LicenseField


class NoAssertionLicense(LicenseField):
    def __init__(self):
        pass
