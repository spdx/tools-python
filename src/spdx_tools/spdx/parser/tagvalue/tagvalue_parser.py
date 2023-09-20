# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from spdx_tools.spdx.model import Document
from spdx_tools.spdx.parser.tagvalue.parser import Parser


def parse_from_file(file_name: str, encoding: str = "utf-8") -> Document:
    parser = Parser()
    with open(file_name, encoding=encoding) as file:
        data = file.read()
    document: Document = parser.parse(data)
    return document
