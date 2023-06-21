# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from beartype.typing import TextIO

from spdx_tools.spdx3.model.software import File
from spdx_tools.spdx3.writer.console.artifact_writer import write_artifact_properties
from spdx_tools.spdx3.writer.console.console import write_value


def write_file(file: File, text_output: TextIO):
    text_output.write("## File\n")
    write_artifact_properties(file, text_output)

    for property_name in File.__annotations__.keys():
        if property_name == "file_purpose":
            write_value(
                property_name, ", ".join([purpose.name for purpose in getattr(file, property_name)]), text_output
            )
            continue
        write_value(property_name, getattr(file, property_name), text_output)
