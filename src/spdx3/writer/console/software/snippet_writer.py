# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from typing import TextIO

from spdx3.model.software.snippet import Snippet
from spdx3.writer.console.artifact_writer import write_artifact_properties
from spdx3.writer.console.console import write_value
from spdx.writer.tagvalue.tagvalue_writer_helper_functions import write_range


def write_snippet(snippet: Snippet, text_output: TextIO):
    text_output.write("## Snippet\n")
    write_artifact_properties(snippet, text_output)
    write_value("content_identifier", snippet.content_identifier, text_output)
    write_value("snippet_purpose", ", ".join([purpose.name for purpose in snippet.snippet_purpose]), text_output)
    write_range("byte_range", snippet.byte_range, text_output)
    write_range("line_range", snippet.line_range, text_output)
