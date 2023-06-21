# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from beartype.typing import TextIO

from spdx_tools.spdx3.model import Hash
from spdx_tools.spdx3.writer.console.console import write_value
from spdx_tools.spdx3.writer.console.integrity_method_writer import write_integrity_method


def write_hash(hash_object: Hash, text_output: TextIO, heading: bool, indent: bool = True):
    if heading:
        text_output.write("## Hash\n")
    write_value("algorithm", hash_object.algorithm, text_output, indent)
    write_value("hash_value", hash_object.hash_value, text_output, indent)
    write_integrity_method(hash_object, text_output, indent)
