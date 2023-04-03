# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from typing import TextIO

from spdx3.model.relationship import Relationship
from spdx3.writer.console.console import write_value
from spdx3.writer.console.element_writer import write_element_properties


def write_relationship(relationship: Relationship, text_output: TextIO):
    text_output.write("## Relationship\n")
    write_element_properties(relationship, text_output)
    write_value("from_element", relationship.from_element, text_output)
    write_value("to", ", ".join(relationship.to), text_output)
    write_value("relationship_type", relationship.relationship_type.name, text_output)
    write_value("completeness", relationship.completeness.name if relationship.completeness else None, text_output)
