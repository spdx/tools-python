# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0


import re
from re import Pattern


class Version:
    VERSION_REGEX: Pattern = re.compile(r"^(\d+)\.(\d+)$")

    major: int
    minor: int

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
        return cls(int(match.group(1)), int(match.group(2)))

    def __init__(self, major: int, minor: int):
        self.major = major
        self.minor = minor

    def __str__(self):
        return f"{self.major}.{self.minor}"

    def __eq__(self, other):
        if not isinstance(other, Version):
            return False
        return self.major == other.major and self.minor == other.minor
