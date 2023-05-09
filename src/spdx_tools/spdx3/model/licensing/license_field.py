# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from abc import ABC, abstractmethod


class LicenseField(ABC):
    @abstractmethod
    def __init__(self):
        pass
