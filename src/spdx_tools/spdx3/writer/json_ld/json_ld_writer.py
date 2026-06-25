# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import json

from spdx_python_model.bindings.v3_0_1 import JSONLDSerializer

from spdx_tools.spdx3.binding.spdx3_to_shacl_converter import Spdx3ToSHACLConverter
from spdx_tools.spdx3.payload import Payload


def write_payload(payload: Payload, file_name: str):
    converter = Spdx3ToSHACLConverter()
    shacl_payload = converter.convert(payload)
    serializer = JSONLDSerializer()
    json_str = serializer.serialize_data(shacl_payload)

    with open(file_name + ".jsonld", "w") as out:
        json.dump(json_str, out, indent=2)
