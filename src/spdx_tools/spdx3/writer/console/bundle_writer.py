# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from beartype.typing import TextIO

from spdx_tools.spdx3.model import Bundle
from spdx_tools.spdx3.writer.console.console import write_value
from spdx_tools.spdx3.writer.console.spdx_collection_writer import write_collection


def write_bundle(bundle: Bundle, text_output: TextIO, heading: bool = True):
    if heading:
        text_output.write("## Bundle\n")
    write_collection(bundle, text_output)
    write_value("context", bundle.context, text_output)
