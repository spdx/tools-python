# SPDX-License-Identifier: Apache-2.0
#
# This file was auto-generated by dev/gen_python_model_from_spec.py
# Do not manually edit!

from beartype.typing import Optional
from enum import Enum, auto


class SoftwareDependencyLinkType(Enum):
    """
    TODO
    """

    STATIC = auto()
    """
    TODOdescription
    """
    DYNAMIC = auto()
    """
    TODOdescription
    """
    TOOL = auto()
    """
    TODOdescription
    """
    OTHER = auto()
    """
    TODOdescription
    """

    def __str__(self) -> str:
        if self == SoftwareDependencyLinkType.STATIC:
            return "static"
        if self == SoftwareDependencyLinkType.DYNAMIC:
            return "dynamic"
        if self == SoftwareDependencyLinkType.TOOL:
            return "tool"
        if self == SoftwareDependencyLinkType.OTHER:
            return "other"
        return "unknown"

    @staticmethod
    def from_str(value: str) -> Optional['SoftwareDependencyLinkType']:
        if value == "static":
            return SoftwareDependencyLinkType.STATIC
        if value == "dynamic":
            return SoftwareDependencyLinkType.DYNAMIC
        if value == "tool":
            return SoftwareDependencyLinkType.TOOL
        if value == "other":
            return SoftwareDependencyLinkType.OTHER
        return None
