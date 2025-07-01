# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import json

from beartype.typing import Any, Dict

from spdx_tools.spdx.model import Document
from spdx_tools.spdx.parser.jsonlikedict.json_like_dict_parser import JsonLikeDictParser

# chars we don't want to see in SBOMs
CONTROL_CHARS_MAP = {
    8: None,  # ASCII/UTF-8: backspace
    12: None,  # ASCII/UTF-8: formfeed
}


def remove_control_chars_from_value(value: Any) -> Any:
    if isinstance(value, str):
        return value.translate(CONTROL_CHARS_MAP)
    elif isinstance(value, list):
        for i in range(len(value)):
            value[i] = remove_control_chars_from_value(value[i])
    return value


def remove_json_control_chars_hook(pairs: list) -> dict:
    return {k: remove_control_chars_from_value(v) for k, v in pairs}


def parse_from_file(file_name: str, encoding: str = "utf-8") -> Document:
    with open(file_name, encoding=encoding) as file:
        input_doc_as_dict: Dict = json.load(file, object_pairs_hook=remove_json_control_chars_hook)

    return JsonLikeDictParser().parse(input_doc_as_dict)
