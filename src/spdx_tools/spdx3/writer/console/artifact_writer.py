# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from beartype.typing import TextIO

from spdx_tools.spdx3.model import Artifact
from spdx_tools.spdx3.writer.console.console import write_value
from spdx_tools.spdx3.writer.console.element_writer import write_element_properties


def write_artifact_properties(artifact: Artifact, text_output: TextIO):
    write_element_properties(artifact, text_output)

    for property_name in Artifact.__annotations__.keys():
        write_value(property_name, getattr(artifact, property_name), text_output)
