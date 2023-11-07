# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import os

from spdx_tools.spdx3.payload import Payload
from spdx_tools.spdx3.parser.json_ld.json_ld_parser import parse_from_string


json_ld = """
{
  "@context": [
    "https://spdx.github.io/spdx-3-model/context.json",
    {
      "myNamespace": "https://some.namespace#",
      "spdxDev": "https://spdx.dev/elements/3F26391C#",
      "spdxLicenses": "https://spdx.org/licenses/"
    }
  ],
  "@graph": [
    {
      "@id": "_:creationInfo1",
      "type": "CreationInfo",
      "specVersion": "3.0.0",
      "created": "2022-12-01T00:00:00Z",
      "createdBy": ["spdxDev:spdx-dev"],
      "profile": ["core", "software"],
      "dataLicense": "spdxLicenses:CC0-1.0"
    },
    {
      "type": "SpdxDocument",
      "spdxId": "myNamespace:spdxdocument159",
      "creationInfo": "_:creationInfo1",
      "name": "Doc 159 - two File elements",
      "element": [
        "myNamespace:SPDXRef-Package",
        "myNamespace:File1",
        "spdxDev:spdx-spec-v2.3",
        "myNamespace:relationship1"
      ],
      "rootElement": [
        "myNamespace:SPDXRef-Package"
      ]
    },
    {
      "type": "Package",
      "spdxId": "myNamespace:SPDXRef-Package",
      "name": "packageName",
      "creationInfo": "_:creationInfo1"
    },
    {
      "type": "File",
      "spdxId": "myNamespace:file1",
      "name": "file1",
      "creationInfo": "_:creationInfo1"
    },
    {
      "type": "File",
      "spdxId": "myNamespace:file2",
      "name": "file2",
      "creationInfo": "_:creationInfo1"
    },
    {
      "type": "Relationship",
      "spdxId": "myNamespace:relationship1",
      "from": "myNamespace:SPDXRef-Package",
      "to": [
        "myNamespace:file1",
        "myNamespace:file2"
      ],
      "relationshipType": "contains",
      "creationInfo": "_:creationInfo1"
    }
  ]
}
"""

# run with:
# $ pytest -vvs tests/spdx3/parser/json_ld/test_json_ld_parser.py::test_json_ld_parser
def test_json_ld_parser():
    payload = parse_from_string(json_ld)
    full_map = payload.get_full_map()

    assert len(full_map) == 5
    assert full_map["https://some.namespace#spdxdocument159"].name == "Doc 159 - two File elements"
