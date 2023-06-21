# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0

from beartype.typing import TextIO

from spdx_tools.spdx3.model.software import SoftwareDependencyRelationship
from spdx_tools.spdx3.writer.console.console import write_value
from spdx_tools.spdx3.writer.console.lifecycle_scoped_relationship_writer import write_lifecycle_scoped_relationship


def write_software_dependency_relationship(
    relationship: SoftwareDependencyRelationship, text_output: TextIO, heading: bool = True
):
    if heading:
        text_output.write("## SoftwareDependencyRelationship\n")
    write_lifecycle_scoped_relationship(relationship, text_output, heading=False)

    for property_name in SoftwareDependencyRelationship.__annotations__.keys():
        write_value(property_name, getattr(relationship, property_name), text_output)
