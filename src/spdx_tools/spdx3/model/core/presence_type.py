# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2024 The SPDX Contributors

from enum import Enum, auto


class PresenceType(Enum):
    NO = auto()
    NO_ASSERTION = auto()
    YES = auto()
