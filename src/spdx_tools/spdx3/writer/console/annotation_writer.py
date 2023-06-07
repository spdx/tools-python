# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from beartype.typing import TextIO

from spdx_tools.spdx3.model import Annotation
from spdx_tools.spdx3.writer.console.console import write_value
from spdx_tools.spdx3.writer.console.element_writer import write_element_properties


def write_annotation(annotation: Annotation, text_output: TextIO):
    text_output.write("## Annotation\n")
    write_element_properties(annotation, text_output)

    for property_name in Annotation.__annotations__.keys():
        write_value(property_name, getattr(annotation, property_name), text_output)
