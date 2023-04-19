# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from typing import TextIO

from spdx_tools.spdx3.model.annotation import Annotation
from spdx_tools.spdx3.writer.console.console import write_value
from spdx_tools.spdx3.writer.console.element_writer import write_element_properties


def write_annotation(annotation: Annotation, text_output: TextIO):
    text_output.write("## Annotation\n")
    write_element_properties(annotation, text_output)
    write_value("annotation_type", annotation.annotation_type.name, text_output)
    write_value("subject", annotation.subject, text_output)
    write_value("content_type", annotation.content_type, text_output)
    write_value("statement", annotation.statement, text_output)
