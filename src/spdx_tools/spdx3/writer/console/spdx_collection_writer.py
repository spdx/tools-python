# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from beartype.typing import TextIO

from spdx_tools.spdx3.model import ElementCollection
from spdx_tools.spdx3.writer.console.element_writer import write_element_properties


def write_collection(collection: ElementCollection, text_output: TextIO):
    write_element_properties(collection, text_output)
    text_output.write(f"elements: {', '.join(collection.element)}\n")
    text_output.write(f"root elements: {', '.join(collection.root_element)}\n")
    text_output.write(f"profile conformance: {', '.join(collection.root_element)}\n")
