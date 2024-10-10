# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from enum import Enum, auto


class ProfileIdentifierType(Enum):
    AI = auto()
    BUILD = auto()
    CORE = auto()
    DATASET = auto()
    EXTENSION = auto()
    LICENSING = auto()
    SECURITY = auto()
    SOFTWARE = auto()
    USAGE = auto()  # Not present in v3.0.1
