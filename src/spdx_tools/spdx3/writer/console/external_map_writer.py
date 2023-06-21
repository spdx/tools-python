# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from beartype.typing import TextIO

from spdx_tools.spdx3.model import ExternalMap
from spdx_tools.spdx3.writer.console.console import write_value
from spdx_tools.spdx3.writer.console.hash_writer import write_hash
from spdx_tools.spdx.writer.tagvalue.tagvalue_writer_helper_functions import write_optional_heading


def write_external_map(external_map: ExternalMap, text_output: TextIO):
    write_value("external_id", external_map.external_id, text_output)
    write_optional_heading(external_map.verified_using, "verified using\n", text_output)
    for integrity_method in external_map.verified_using:
        # for now Hash is the only child class of the abstract class IntegrityMethod,
        # as soon as there are more inherited classes we need to implement a logic
        # that determines the correct write function for the "integrity_method" object
        write_hash(integrity_method, text_output, heading=False)
    write_value("location_hint", external_map.location_hint, text_output)
