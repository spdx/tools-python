# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from beartype.typing import TextIO

from spdx_tools.spdx3.model import SpdxDocument
from spdx_tools.spdx3.writer.console.bundle_writer import write_bundle


def write_spdx_document(spdx_document: SpdxDocument, text_output: TextIO):
    text_output.write("## SPDX Document\n")
    write_bundle(spdx_document, text_output, False)
