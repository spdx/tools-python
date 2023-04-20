# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from typing import TextIO

from spdx_tools.spdx3.model.software import File
from spdx_tools.spdx3.writer.console.artifact_writer import write_artifact_properties
from spdx_tools.spdx3.writer.console.console import write_value


def write_file(file: File, text_output: TextIO):
    text_output.write("## File\n")
    write_artifact_properties(file, text_output)
    write_value("content_identifier", file.content_identifier, text_output)
    write_value("file_purpose", ", ".join([purpose.name for purpose in file.file_purpose]), text_output)
    write_value("content_type", file.content_type, text_output)
