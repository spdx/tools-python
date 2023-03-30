# SPDX-FileCopyrightText: 2023 spdx contributors

# SPDX-License-Identifier: Apache-2.0
from spdx.model.document import Document
from spdx.parser.tagvalue.parser import Parser


def parse_from_file(file_name: str) -> Document:
    parser = Parser()
    with open(file_name) as file:
        data = file.read()
    document: Document = parser.parse(data)
    return document
