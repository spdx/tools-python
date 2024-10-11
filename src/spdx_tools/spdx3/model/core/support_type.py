# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2024 The SPDX Contributors

from enum import Enum, auto


class SupportType(Enum):
    DEPLOYED = auto()
    DEVELOPMENT = auto()
    END_OF_SUPPORT = auto()
    LIMITED_SUPPORT = auto()
    NO_ASSERTION = auto()
    NO_SUPPORT = auto()
    SUPPORT = auto()
