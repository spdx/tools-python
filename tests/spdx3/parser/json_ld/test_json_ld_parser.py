# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import os

from spdx_tools.spdx3.payload import Payload
from spdx_tools.spdx3.parser.json_ld.json_ld_parser import parse_from_string, GraphToElementConverter
from rdflib import Graph, URIRef, Literal, BNode
from semantic_version import Version
from spdx_tools.spdx.datetime_conversions import datetime_from_str


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

json_ld_small = """
{
  "@context": "https://spdx.github.io/spdx-3-model/context.json",
  "type": "SpdxDocument",
  "spdxId": "http://spdx.acme.org/3FA9CB25#spdxdocument159",
  "creationInfo": {
    "@id": "_:creationInfo1",
    "type": "CreationInfo",
    "specVersion": "3.0.0",
    "created": "2022-12-01T00:00:00Z",
    "createdBy": ["https://spdx.dev/elements/3F26391C#spdx-dev"],
    "profile": ["core", "software"],
    "dataLicense": "https://spdx.org/licenses/CC0-1.0"
  },
  "name": "Doc 159 - two File elements",
  "element": [
    "https://some.namespace#File1",
    "https://spdx.dev/elements/3F26391C#spdx-spec-v2.3"
  ],
  "rootElement": [
    "https://some.namespace#File1"
  ]
}
"""

def test_json_ld_converter_small():
    graph = Graph().parse(data=json_ld_small, format='json-ld')
    converter = GraphToElementConverter(graph)

    documentSubject = URIRef("http://spdx.acme.org/3FA9CB25#spdxdocument159")
    assert converter.getGraphSpdxValue(documentSubject, "Core", "name") == "Doc 159 - two File elements"

    creationInfoSubject = BNode("creationInfo1")
    assert converter.getGraphSpdxValues(creationInfoSubject, "Core", "createdBy") == [URIRef("https://spdx.dev/elements/3F26391C#spdx-dev")] 
    assert converter.getGraphSpdxValueAsVersion(creationInfoSubject, "Core", "specVersion") == Version("3.0.0")
    assert converter.getGraphSpdxValueAsDatetime(creationInfoSubject, "Core", "created") == datetime_from_str("2022-12-01T00:00:00Z")

def test_json_ld_parser_small():
    payload = parse_from_string(json_ld_small)
    full_map = payload.get_full_map()

    assert len(full_map) == 1
    assert full_map["http://spdx.acme.org/3FA9CB25#spdxdocument159"].name == "Doc 159 - two File elements"
