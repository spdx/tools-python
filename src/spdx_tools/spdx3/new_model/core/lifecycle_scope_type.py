# SPDX-License-Identifier: Apache-2.0
#
# This file was auto-generated by dev/gen_python_model_from_spec.py
# Do not manually edit!

from beartype.typing import Optional
from enum import Enum, auto


class LifecycleScopeType(Enum):
    """
    TODO
    """

    DESIGN = auto()
    """
    TODOdescription
    """
    BUILD = auto()
    """
    TODOdescription
    """
    DEVELOPMENT = auto()
    """
    TODOdescription
    """
    TEST = auto()
    """
    TODOdescription
    """
    RUNTIME = auto()
    """
    TODOdescription
    """
    OTHER = auto()
    """
    TODOdescription
    """

    def __str__(self) -> str:
        if self == LifecycleScopeType.DESIGN:
            return "design"
        if self == LifecycleScopeType.BUILD:
            return "build"
        if self == LifecycleScopeType.DEVELOPMENT:
            return "development"
        if self == LifecycleScopeType.TEST:
            return "test"
        if self == LifecycleScopeType.RUNTIME:
            return "runtime"
        if self == LifecycleScopeType.OTHER:
            return "other"
        return "unknown"

    @staticmethod
    def from_str(value: str) -> Optional['LifecycleScopeType']:
        if value == "design":
            return LifecycleScopeType.DESIGN
        if value == "build":
            return LifecycleScopeType.BUILD
        if value == "development":
            return LifecycleScopeType.DEVELOPMENT
        if value == "test":
            return LifecycleScopeType.TEST
        if value == "runtime":
            return LifecycleScopeType.RUNTIME
        if value == "other":
            return LifecycleScopeType.OTHER
        return None
