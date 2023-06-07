# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from datetime import datetime
from enum import Enum

from beartype.typing import Any, List
from semantic_version import Version

from spdx_tools.spdx3.model.creation_info import CreationInfo
from spdx_tools.spdx3.model.hash import Hash
from spdx_tools.spdx3.payload import Payload
from spdx_tools.spdx.casing_tools import snake_case_to_camel_case
from spdx_tools.spdx.datetime_conversions import datetime_to_iso_string


def convert_payload_to_json_ld_list_of_elements(payload: Payload) -> List:
    element_list = []

    for element in payload.get_full_map().values():
        element_dict = _convert_to_json_ld_dict(element)
        element_list.append(element_dict)

    return element_list


def _convert_to_json_ld_dict(element: Any, alt_creation_info=False, alt_hash=False):
    if not element:
        return None

    if isinstance(element, (str, int, tuple)):
        return element

    if isinstance(element, Version):
        return str(element)

    if isinstance(element, datetime):
        return datetime_to_iso_string(element)

    if isinstance(element, Enum):
        return snake_case_to_camel_case(element.name)

    if isinstance(element, list):
        return [_convert_to_json_ld_dict(item) for item in element if item]

    if alt_hash and isinstance(element, Hash):
        hash_dict = {element.algorithm.name: element.hash_value}
        if element.comment:
            hash_dict["comment"] = element.comment
        return hash_dict

    # if issubclass(element.__class__, Element):
    #     element_dict = {"@type": element.__class__.__name__}
    # else:
    #     element_dict = {}  # typing of non-Element classes should be handled by the @context, I think

    element_dict = {"@type": element.__class__.__name__}

    for attribute_name in vars(element):
        attribute_value = getattr(element, attribute_name)

        if alt_creation_info and isinstance(attribute_value, CreationInfo):
            for creation_info_attr_name in vars(attribute_value):
                creation_info_attr_value = getattr(attribute_value, creation_info_attr_name)
                element_dict[snake_case_to_camel_case(creation_info_attr_name)] = _convert_to_json_ld_dict(
                    creation_info_attr_value
                )

        elif attribute_value:
            if attribute_name == "_spdx_id":
                attribute_name = "@id"
            elif attribute_name == "_from_element":
                attribute_name = "from"
            else:
                attribute_name = snake_case_to_camel_case(attribute_name)

            element_dict[attribute_name] = _convert_to_json_ld_dict(attribute_value)

    return element_dict
