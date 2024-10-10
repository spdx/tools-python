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
    DEVICE_DRIVER = auto()
    DISK_IMAGE = auto()
    DOCUMENTATION = auto()
    EVIDENCE = auto()
    EXECUTABLE = auto()
    FILE = auto()
    FILESYSTEM_IMAGE = auto()
    FIRMWARE = auto()
    FRAMEWORK = auto()
    INSTALL = auto()
    LIBRARY = auto()
    MANIFEST = auto()
    MODEL = auto()
    MODULE = auto()
    OPERATING_SYSTEM = auto()
    OTHER = auto()
    PATCH = auto()
    PLATFORM = auto()
    REQUIREMENT = auto()
    SOURCE = auto()
    SPECIFICATION = auto()
    TEST = auto()
