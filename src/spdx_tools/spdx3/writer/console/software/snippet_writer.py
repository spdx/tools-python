# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from beartype.typing import TextIO

from spdx_tools.spdx3.model.software import Snippet
from spdx_tools.spdx3.writer.console.artifact_writer import write_artifact_properties
from spdx_tools.spdx3.writer.console.console import write_value


def write_snippet(snippet: Snippet, text_output: TextIO):
    text_output.write("## Snippet\n")
    write_artifact_properties(snippet, text_output)

    for property_name in Snippet.__annotations__.keys():
        if property_name == "snippet_purpose":
            write_value(
                property_name, ", ".join([purpose.name for purpose in getattr(snippet, property_name)]), text_output
            )
            continue
        write_value(property_name, getattr(snippet, property_name), text_output)
