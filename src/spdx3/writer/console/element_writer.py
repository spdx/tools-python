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
from spdx3.model.element import Element
from spdx3.writer.console.console import write_value
from spdx3.writer.console.creation_information_writer import write_creation_info
from spdx3.writer.console.external_identifier_writer import write_external_identifier
from spdx3.writer.console.external_reference_writer import write_external_reference
from spdx3.writer.console.hash_writer import write_hash


def write_element_properties(element: Element, text_output: TextIO):
    write_value("SPDXID", element.spdx_id, text_output)
    write_value("name", element.name, text_output)
    write_creation_info(element.creation_info, text_output, True)
    write_value("summary", element.summary, text_output)
    write_value("description", element.description, text_output)
    write_value("comment", element.comment, text_output)
    write_optional_heading(element.verified_using, "verified using:\n", text_output)
    for integrity_method in element.verified_using:
        # for now Hash is the only child class of the abstract class IntegrityMethod, as soon as there are more inherited
        # classes we need to implement a logic that determines the correct write function for the "integrity_method" object
        write_hash(integrity_method, text_output, heading=False)
    write_optional_heading(element.external_references, "External References", text_output)
    for external_reference in element.external_references:
        write_external_reference(external_reference, text_output)
    write_optional_heading(element.external_identifier, "External Identifier", text_output)
    for external_identifier in element.external_identifier:
        write_external_identifier(external_identifier, text_output)
