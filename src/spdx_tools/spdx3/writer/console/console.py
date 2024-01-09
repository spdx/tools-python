# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from enum import Enum

from beartype.typing import Optional, TextIO, Union


def write_value(tag: str, value: Optional[Union[bool, str, dict, list, Enum]], out: TextIO, indent: bool = False):
    """This function is duplicated from spdx_tools.spdx.writer.tagvalue.tag_value_writer_helper_functions
    and slightly adapted to make indentation of output possible."""
    if not value:
        return
    if isinstance(value, dict):
        value = ", ".join([f"{tag}: ({key}: {val})" for key, val in value.items()])
    if isinstance(value, list):
        value = ", ".join([entry for entry in value])
    if isinstance(value, Enum):
        value = value.name
    write_and_possibly_indent(f"{tag}: {value}", indent, out)


def write_and_possibly_indent(text: str, indent: bool, out: TextIO):
    if indent:
        out.write(f"  {text}\n")
    else:
        out.write(f"{text}\n")
