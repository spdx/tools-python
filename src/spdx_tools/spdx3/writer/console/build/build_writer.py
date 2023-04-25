# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from typing import TextIO

from spdx_tools.spdx3.model.build import Build
from spdx_tools.spdx3.writer.console.console import write_dict, write_value
from spdx_tools.spdx3.writer.console.element_writer import write_element_properties
from spdx_tools.spdx3.writer.console.hash_writer import write_hash
from spdx_tools.spdx.writer.tagvalue.tagvalue_writer_helper_functions import write_optional_heading


def write_build(build: Build, text_output: TextIO):
    text_output.write("## Build\n")
    write_element_properties(build, text_output)

    write_value("build_type", build.build_type, text_output)
    write_value("build_id", build.build_id, text_output)
    write_value("config_source_entrypoint", ", ".join([entry for entry in build.config_source_entrypoint]),
                text_output)
    write_value("config_source_uri", ", ".join([entry for entry in build.config_source_uri]), text_output)
    write_optional_heading(build.config_source_digest, "config_source_digest", text_output)
    for digest_hash in build.config_source_digest:
        write_hash(digest_hash, text_output, heading=False)
    write_dict("parameters", build.parameters, text_output)
    write_value("build_start", build.build_start, text_output)
    write_value("build_end", build.build_end, text_output)
    write_dict("environment", build.environment, text_output)
