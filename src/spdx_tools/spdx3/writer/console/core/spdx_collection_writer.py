# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from beartype.typing import TextIO

from spdx_tools.spdx3.model.core import ElementCollection
from spdx_tools.spdx3.writer.console.core import (
    write_element_properties,
    write_external_map,
    write_namespace_map,
)
from spdx_tools.spdx.writer.tagvalue.tagvalue_writer_helper_functions import (
    write_optional_heading,
)


def write_collection(collection: ElementCollection, text_output: TextIO):
    write_element_properties(collection, text_output)
    text_output.write(f"elements: {', '.join(collection.element)}\n")
    write_optional_heading(collection.namespace, "# Namespace\n", text_output)
    for namespace_map in collection.namespace:
        write_namespace_map(namespace_map, text_output)
    write_optional_heading(collection.import_, "# Import\n", text_output)
    for external_map in collection.import_:
        write_external_map(external_map, text_output)
