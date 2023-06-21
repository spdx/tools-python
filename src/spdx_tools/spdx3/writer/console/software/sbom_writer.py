# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from beartype.typing import TextIO

from spdx_tools.spdx3.model.software import Sbom
from spdx_tools.spdx3.writer.console.bom_writer import write_bom


def write_sbom(sbom: Sbom, text_output: TextIO):
    text_output.write("## Sbom\n")
    write_bom(sbom, text_output, False)
