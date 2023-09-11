# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import json

from beartype.typing import Dict

from spdx_tools.spdx.model import Document
from spdx_tools.spdx.parser.jsonlikedict.json_like_dict_parser import JsonLikeDictParser


def parse_from_file(file_name: str, encoding: str = "utf-8") -> Document:
    with open(file_name, encoding=encoding) as file:
        input_doc_as_dict: Dict = json.load(file)

    return JsonLikeDictParser().parse(input_doc_as_dict)
