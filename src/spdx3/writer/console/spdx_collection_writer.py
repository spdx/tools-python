# Copyright (c) 2023 spdx contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#   http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from typing import TextIO

from spdx.writer.tagvalue.tagvalue_writer_helper_functions import write_optional_heading
from spdx3.model.spdx_collection import SpdxCollection
from spdx3.writer.console.element_writer import write_element_properties
from spdx3.writer.console.external_map_writer import write_external_map
from spdx3.writer.console.namespace_map_writer import write_namespace_map


def write_collection(collection: SpdxCollection, text_output: TextIO):
    write_element_properties(collection, text_output)
    text_output.write(f"elements: {', '.join(collection.elements)}\n")
    write_optional_heading(collection.namespaces, "# Namespaces\n", text_output)
    for namespace_map in collection.namespaces:
        write_namespace_map(namespace_map, text_output)
    write_optional_heading(collection.imports, "# Imports\n", text_output)
    for external_map in collection.imports:
        write_external_map(external_map, text_output)
