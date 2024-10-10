# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import json
import os

from spdx_tools.spdx3.payload import Payload
from spdx_tools.spdx3.writer.json_ld.json_ld_converter import convert_payload_to_json_ld_list_of_elements


def write_payload(payload: Payload, file_name: str):
    element_list = convert_payload_to_json_ld_list_of_elements(payload)

    # this will be obsolete as soon as the context is publicly available under some URI
    # Use the context file from https://spdx.github.io/spdx-spec/v3.0.1/serializations/#json-ld-context-file
    with open(os.path.join(os.path.dirname(__file__), "context.json"), "r") as infile:
        data = json.load(infile)
        context = data.get("@context")

    complete_dict = {"@context": context, "@graph": element_list}

    with open(file_name + ".jsonld", "w") as out:
        json.dump(complete_dict, out, indent=2)
