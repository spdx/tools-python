# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0

from typing import Optional, TextIO, Union


def write_value(tag: str, value: Optional[Union[bool, str]], out: TextIO, indent: bool = False):
    """This function is duplicated from spdx.writer.tagvalue.tag_value_writer_helper_functions and slightly adapted to
    make indentation of output possible."""
    if not value:
        return
    if indent:
        out.write(f"\t{tag}: {value}\n")
    else:
        out.write(f"{tag}: {value}\n")
