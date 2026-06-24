import json
from typing import Dict

from spdx_python_model import v3_0_1 as spdx_3_0

from spdx_tools.spdx3.binding.shacl_to_spdx3_converter import convert_to_payload
from spdx_tools.spdx3.payload import Payload


def parse_from_file(file_name: str) -> Payload:
    object_set = spdx_3_0.SHACLObjectSet()

    with open(file_name, "r") as fd:
        sbom: Dict = json.load(fd)
        spdx_3_0.JSONLDDeserializer().deserialize_data(sbom, object_set)

    return convert_to_payload(object_set)


def parse_from_string(json_string: str) -> Payload:
    object_set = spdx_3_0.SHACLObjectSet()

    sbom: Dict = json.loads(json_string)
    spdx_3_0.JSONLDDeserializer().deserialize_data(sbom, object_set)

    return convert_to_payload(object_set)
