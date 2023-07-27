# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0

from .general_templates import FILE_HEADER

VOCAB_FILE = FILE_HEADER + """from beartype.typing import Optional
from enum import Enum, auto


class {typename}(Enum):{docstring}

{values}

    def __str__(self) -> str:
{values_to_str}
        return "unknown"

    @staticmethod
    def from_str(value: str) -> Optional['{typename}']:
{str_to_values}
        return None
"""

VOCAB_ENTRY = "    {value} = auto(){docstring}"
VOCAB_VALUE_TO_STR = "        if self == {typename}.{python_value}:\n            return \"{str_value}\""
VOCAB_STR_TO_VALUE = "        if value == \"{str_value}\":\n            return {typename}.{python_value}"
