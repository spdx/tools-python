# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from typing import TextIO

from spdx_tools.spdx3.model import Relationship
from spdx_tools.spdx3.writer.console.console import write_value
from spdx_tools.spdx3.writer.console.element_writer import write_element_properties


def write_relationship(relationship: Relationship, text_output: TextIO):
    text_output.write("## Relationship\n")
    write_element_properties(relationship, text_output)
    for property_name in relationship.__annotations__.keys():
        write_value(property_name, getattr(relationship, property_name), text_output)
