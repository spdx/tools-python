# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import json
from importlib import resources

from spdx_tools.spdx3.payload import Payload
from spdx_tools.spdx3.writer.json_ld.json_ld_converter import (
    convert_payload_to_json_ld_list_of_elements,
)


def write_payload(payload: Payload, file_name: str):
    element_list = convert_payload_to_json_ld_list_of_elements(payload)

    # this will be obsolete as soon as the context is publicly available under some URI
    # Note: 3.0.1 context is now available at
    # https://spdx.org/rdf/3.0.1/spdx-context.jsonld
    with resources.files("spdx_tools.spdx3.writer.json_ld").joinpath("context.json").open("r") as infile:
        context = json.load(infile)

    complete_dict = {"@context": context, "@graph": element_list}

    with open(file_name + ".jsonld", "w", encoding="utf-8") as out:
        json.dump(complete_dict, out, indent=2)
