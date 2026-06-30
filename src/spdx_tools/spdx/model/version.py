# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0


import re
from re import Pattern


class Version:
    VERSION_REGEX: Pattern = re.compile(r"^(\d+)\.(\d+)(?:\.(\d+))?$")

    major: int
    minor: int
    patch: int | None

    @classmethod
    def is_valid_version_string(cls, value: str) -> bool:
        return cls.VERSION_REGEX.match(value) is not None

    # No type hint for Python reasons.
    # See https://stackoverflow.com/questions/33533148/how-do-i-type-hint-a-method-with-the-type-of-the-enclosing-class
    @classmethod
    def from_string(cls, value: str):
        if not Version.is_valid_version_string(value):
            raise ValueError(f"{value} is not a valid version string")

        match = cls.VERSION_REGEX.match(value)
        major = int(match.group(1))
        minor = int(match.group(2))
        patch = int(match.group(3)) if match.group(3) else None
        return cls(major, minor, patch)

    def __init__(self, major: int, minor: int, patch: int | None = None):
        self.major = major
        self.minor = minor
        self.patch = patch

    def __str__(self):
        patch_suffix = f".{self.patch}" if self.patch is not None else ""
        return f"{self.major}.{self.minor}{patch_suffix}"

    def __eq__(self, other):
        if not isinstance(other, Version):
            return False
        return self.major == other.major and self.minor == other.minor and self.patch == other.patch
