# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from enum import Enum, auto


class SoftwarePurpose(Enum):
    APPLICATION = auto()
    ARCHIVE = auto()
    BOM = auto()
    CONFIGURATION = auto()
    CONTAINER = auto()
    DATA = auto()
    DEVICE = auto()
    DOCUMENTATION = auto()
    EXECUTABLE = auto()
    FILE = auto()
    FIRMWARE = auto()
    FRAMEWORK = auto()
    INSTALL = auto()
    LIBRARY = auto()
    MODEL = auto()
    MODULE = auto()
    OPERATING_SYSTEM = auto()
    OTHER = auto()
    PATCH = auto()
    REQUIREMENT = auto()
    SOURCE = auto()
    TEST = auto()
