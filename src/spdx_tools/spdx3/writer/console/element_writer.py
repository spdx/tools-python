# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from beartype.typing import TextIO

from spdx_tools.spdx3.model import Element
from spdx_tools.spdx3.writer.console.console import write_value
from spdx_tools.spdx3.writer.console.creation_info_writer import write_creation_info
from spdx_tools.spdx3.writer.console.external_identifier_writer import write_external_identifier
from spdx_tools.spdx3.writer.console.external_reference_writer import write_external_reference
from spdx_tools.spdx3.writer.console.hash_writer import write_hash
from spdx_tools.spdx.writer.tagvalue.tagvalue_writer_helper_functions import write_optional_heading


def write_element_properties(element: Element, text_output: TextIO):
    write_value("SPDXID", element.spdx_id, text_output)
    write_value("name", element.name, text_output)
    if element.creation_info:
        write_creation_info(element.creation_info, text_output, True)
    write_value("summary", element.summary, text_output)
    write_value("description", element.description, text_output)
    write_value("comment", element.comment, text_output)
    write_optional_heading(element.verified_using, "verified using:\n", text_output)
    for integrity_method in element.verified_using:
        # for now Hash is the only child class of the abstract class IntegrityMethod,
        # as soon as there are more inherited classes we need to implement a logic
        # that determines the correct write function for the "integrity_method" object
        write_hash(integrity_method, text_output, heading=False)
    write_optional_heading(element.external_reference, "External Reference\n", text_output)
    for external_reference in element.external_reference:
        write_external_reference(external_reference, text_output)
    write_optional_heading(element.external_identifier, "External Identifier\n", text_output)
    for external_identifier in element.external_identifier:
        write_external_identifier(external_identifier, text_output)
