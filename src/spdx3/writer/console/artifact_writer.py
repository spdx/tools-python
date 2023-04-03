# SPDX-FileCopyrightText: 2023 spdx contributors

# SPDX-License-Identifier: Apache-2.0
from typing import TextIO

from spdx3.model.artifact import Artifact
from spdx3.writer.console.console import write_value
from spdx3.writer.console.element_writer import write_element_properties


def write_artifact_properties(artifact: Artifact, text_output: TextIO):
    write_element_properties(artifact, text_output)
    write_value("originated_by", artifact.originated_by, text_output)
