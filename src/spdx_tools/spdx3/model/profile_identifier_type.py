# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from enum import Enum, auto


class ProfileIdentifierType(Enum):
    CORE = auto()
    SOFTWARE = auto()
    EXPANDED_LICENSING = auto()
    SECURITY = auto()
    BUILD = auto()
    AI = auto()
    DATASET = auto()
    EXTENSION = auto()
    LITE = auto()
    SIMPLE_LICENSING = auto()
