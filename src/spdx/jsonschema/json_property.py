# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from enum import Enum


class JsonProperty(Enum):
    """
    Parent class for all json property classes. Not meant to be instantiated directly, only to have a common parent
    type that can be used in type hints.
    In general, all the child enums list the properties of the corresponding objects from the json schema.
    """

    pass
