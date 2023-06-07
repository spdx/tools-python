# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from beartype.typing import TextIO

from spdx_tools.spdx3.model.build import Build
from spdx_tools.spdx3.writer.console.console import write_value
from spdx_tools.spdx3.writer.console.element_writer import write_element_properties
from spdx_tools.spdx3.writer.console.hash_writer import write_hash
from spdx_tools.spdx.writer.tagvalue.tagvalue_writer_helper_functions import write_optional_heading


def write_build(build: Build, text_output: TextIO):
    text_output.write("## Build\n")
    write_element_properties(build, text_output)

    for property_name in Build.__annotations__.keys():
        if property_name == "config_source_digest":
            write_optional_heading(build.config_source_digest, "config_source_digest", text_output)
            for digest_hash in build.config_source_digest:
                write_hash(digest_hash, text_output, heading=False)
            continue

        write_value(property_name, getattr(build, property_name), text_output)
