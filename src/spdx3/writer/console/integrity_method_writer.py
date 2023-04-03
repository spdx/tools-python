# SPDX-FileCopyrightText: 2023 spdx contributors

# SPDX-License-Identifier: Apache-2.0
from typing import TextIO

from spdx3.model.integrity_method import IntegrityMethod
from spdx3.writer.console.console import write_value


def write_integrity_method(integrity_method: IntegrityMethod, text_output: TextIO, indent: bool = True):
    write_value("comment", integrity_method.comment, text_output, indent)
