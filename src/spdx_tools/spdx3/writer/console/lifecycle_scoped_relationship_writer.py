# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0

from beartype.typing import TextIO

from spdx_tools.spdx3.model import LifecycleScopedRelationship
from spdx_tools.spdx3.writer.console.console import write_value
from spdx_tools.spdx3.writer.console.relationship_writer import write_relationship


def write_lifecycle_scoped_relationship(
    relationship: LifecycleScopedRelationship, text_output: TextIO, heading: bool = True
):
    if heading:
        text_output.write("## LifecycleScopedRelationship\n")
    write_relationship(relationship, text_output, heading=False)

    for property_name in LifecycleScopedRelationship.__annotations__.keys():
        write_value(property_name, getattr(relationship, property_name), text_output)
