# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import json
from typing import Union

from beartype.typing import Dict, List
from semantic_version import Version

from spdx_tools.spdx3.model import HashAlgorithm
from spdx_tools.spdx3.parser.model_definition_dicts import (
    CLASS_DICT,
    DATETIME_PROPERTIES,
    ENUM_DICT,
    KEYS_WITH_URI_VALUES,
    SPECIALLY_TREATED_KEYS,
    VERSION_PROPERTIES,
)
from spdx_tools.spdx3.payload import Payload
from spdx_tools.spdx.casing_tools import camel_case_to_snake_case
from spdx_tools.spdx.datetime_conversions import datetime_from_str


def parse_from_file(file_name: str) -> Payload:
    with open(file_name) as file:
        input_as_dict: Dict = json.load(file)

    context = input_as_dict["@context"]
    custom_context = {}
    if isinstance(context, list):
        for entry in context:
            if isinstance(entry, dict):
                custom_context.update(entry)

    if "@graph" in input_as_dict:
        payload = parse_list_of_elements(input_as_dict["@graph"], custom_context)
    else:  # in case of only a single serialized element
        input_as_dict.pop("@context")
        payload = Payload()
        payload.add_element(parse_element_object(input_as_dict, custom_context))

    return payload


def parse_list_of_elements(list_of_elements: List[Dict], custom_context: Dict):
    payload = Payload()
    for element_object in list_of_elements:
        payload.add_element(parse_element_object(element_object, custom_context))
    return payload


def parse_element_object(element_object: Union[Dict, str], custom_context: Dict):
    if isinstance(element_object, str):
        return element_object

    element_properties = {}
    if "@id" in element_object:
        element_properties["spdx_id"] = expand_uri(element_object.pop("@id"), custom_context)

    element_type = element_object.pop("type")

    for key, value in element_object.items():
        if key in ENUM_DICT:
            value = parse_enum_property(key, value)
        elif isinstance(value, dict):
            value = parse_element_object(value, custom_context)
        elif isinstance(value, list):
            value = [parse_element_object(entry, custom_context) for entry in value]
        elif key in VERSION_PROPERTIES:
            value = Version(value)
        elif key in DATETIME_PROPERTIES:
            value = datetime_from_str(value)

        if key in KEYS_WITH_URI_VALUES:
            if isinstance(value, list):
                value = [expand_uri(entry, custom_context) for entry in value]
            else:
                value = expand_uri(value, custom_context)

        if key in SPECIALLY_TREATED_KEYS:
            element_properties[SPECIALLY_TREATED_KEYS[key]] = value
        else:
            element_properties[camel_case_to_snake_case(key)] = value

    if element_type not in CLASS_DICT:
        raise ValueError(f"element type {element_type} not found in CLASS_DICT. Maybe it was forgotten?")
    return CLASS_DICT[element_type](**element_properties)


def expand_uri(spdx_id, custom_context):
    if ":" in spdx_id:
        prefix, suffix = spdx_id.split(":", 1)
        if prefix in custom_context and not suffix.startswith("//"):
            spdx_id = custom_context[prefix] + suffix
    return spdx_id


def parse_enum_property(key: str, value: str):
    enum_class = ENUM_DICT[key]
    if enum_class == HashAlgorithm:
        return parse_hash_algorithm(value)
    if isinstance(value, str):
        return enum_class[camel_case_to_snake_case(value).upper()]
    elif isinstance(value, list):
        return [enum_class[camel_case_to_snake_case(entry).upper()] for entry in value]
    else:
        raise ValueError(f"unrecognized Enum property: {key}: {value}")


def parse_hash_algorithm(value: str):
    if value.startswith("blake"):
        return HashAlgorithm[value.upper()]

    return HashAlgorithm[camel_case_to_snake_case(value).upper()]
