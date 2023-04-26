# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import json

from spdx_tools.spdx3.payload import Payload
from spdx_tools.spdx3.writer.json_ld.json_ld_converter import convert_payload_to_json_ld_list_of_elements


def write_payload(payload: Payload, file_name: str):
    element_list = convert_payload_to_json_ld_list_of_elements(payload)

    # this will be obsolete as soon as the context is publicly available under some URI
    with open("context.json", "r") as infile:
        context = json.load(infile)

    complete_dict = {"@context": context, "element": element_list}

    with open(file_name, "w") as out:
        json.dump(complete_dict, out, indent=2)
