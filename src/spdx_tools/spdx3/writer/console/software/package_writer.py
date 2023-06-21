# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from beartype.typing import TextIO

from spdx_tools.spdx3.model.software import Package
from spdx_tools.spdx3.writer.console.artifact_writer import write_artifact_properties
from spdx_tools.spdx3.writer.console.console import write_value


def write_package(package: Package, text_output: TextIO, heading: bool = True):
    if heading:
        text_output.write("## Package\n")
    write_artifact_properties(package, text_output)

    for property_name in Package.__annotations__.keys():
        if property_name == "package_purpose":
            write_value(
                property_name, ", ".join([purpose.name for purpose in getattr(package, property_name)]), text_output
            )
            continue
        write_value(property_name, getattr(package, property_name), text_output)
