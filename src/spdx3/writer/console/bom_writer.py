# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from typing import TextIO

from spdx3.model.bom import Bom
from spdx3.writer.console.bundle_writer import write_bundle


def write_bom(bom: Bom, text_output: TextIO, heading: bool = True):
    if heading:
        text_output.write("## Bom\n")
    write_bundle(bom, text_output, False)
