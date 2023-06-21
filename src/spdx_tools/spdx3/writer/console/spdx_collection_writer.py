# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from beartype.typing import TextIO

from spdx_tools.spdx3.model import ElementCollection
from spdx_tools.spdx3.writer.console.element_writer import write_element_properties
from spdx_tools.spdx3.writer.console.external_map_writer import write_external_map
from spdx_tools.spdx3.writer.console.namespace_map_writer import write_namespace_map
from spdx_tools.spdx.writer.tagvalue.tagvalue_writer_helper_functions import write_optional_heading


def write_collection(collection: ElementCollection, text_output: TextIO):
    write_element_properties(collection, text_output)
    text_output.write(f"elements: {', '.join(collection.element)}\n")
    write_optional_heading(collection.namespaces, "# Namespaces\n", text_output)
    for namespace_map in collection.namespaces:
        write_namespace_map(namespace_map, text_output)
    write_optional_heading(collection.imports, "# Imports\n", text_output)
    for external_map in collection.imports:
        write_external_map(external_map, text_output)
