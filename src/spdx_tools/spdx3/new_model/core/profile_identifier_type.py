# SPDX-License-Identifier: Apache-2.0
#
# This file was auto-generated by dev/gen_python_model_from_spec.py
# Do not manually edit!
# flake8: noqa

from enum import Enum, auto

from beartype.typing import Optional


class ProfileIdentifierType(Enum):
    """
    There are a set of profiles that have been defined to be valid for a specific release This file enumerates the
    values that have been agreed on, and may be applied to the creation information for an an element.
    """

    CORE = auto()
    """
    the element follows the Core profile specification
    """
    SOFTWARE = auto()
    """
    the element follows the Software profile specification
    """
    SIMPLE_LICENSING = auto()
    """
    the element follows the simple Licensing profile specification
    """
    EXPANDED_LICENSING = auto()
    """
    the element follows the expanded Licensing profile specification
    """
    SECURITY = auto()
    """
    the element follows the Security profile specification
    """
    BUILD = auto()
    """
    the element follows the Build profile specification
    """
    AI = auto()
    """
    the element follows the AI profile specification
    """
    DATASET = auto()
    """
    the element follows the Dataset profile specification
    """
    USAGE = auto()
    """
    the element follows the Usage profile specification
    """
    EXTENSION = auto()
    """
    the element follows the Extension profile specification
    """

    def __str__(self) -> str:
        if self == ProfileIdentifierType.CORE:
            return "core"
        if self == ProfileIdentifierType.SOFTWARE:
            return "software"
        if self == ProfileIdentifierType.SIMPLE_LICENSING:
            return "simpleLicensing"
        if self == ProfileIdentifierType.EXPANDED_LICENSING:
            return "expandedLicensing"
        if self == ProfileIdentifierType.SECURITY:
            return "security"
        if self == ProfileIdentifierType.BUILD:
            return "build"
        if self == ProfileIdentifierType.AI:
            return "ai"
        if self == ProfileIdentifierType.DATASET:
            return "dataset"
        if self == ProfileIdentifierType.USAGE:
            return "usage"
        if self == ProfileIdentifierType.EXTENSION:
            return "extension"
        return "unknown"

    @staticmethod
    def from_str(value: str) -> Optional["ProfileIdentifierType"]:
        if value == "core":
            return ProfileIdentifierType.CORE
        if value == "software":
            return ProfileIdentifierType.SOFTWARE
        if value == "simpleLicensing":
            return ProfileIdentifierType.SIMPLE_LICENSING
        if value == "expandedLicensing":
            return ProfileIdentifierType.EXPANDED_LICENSING
        if value == "security":
            return ProfileIdentifierType.SECURITY
        if value == "build":
            return ProfileIdentifierType.BUILD
        if value == "ai":
            return ProfileIdentifierType.AI
        if value == "dataset":
            return ProfileIdentifierType.DATASET
        if value == "usage":
            return ProfileIdentifierType.USAGE
        if value == "extension":
            return ProfileIdentifierType.EXTENSION
        return None
