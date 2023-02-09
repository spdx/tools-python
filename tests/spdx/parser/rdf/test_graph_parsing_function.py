# Copyright (c) 2023 spdx contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import pytest
from rdflib import URIRef, Graph, Namespace

from spdx.parser.rdf.graph_parsing_functions import parse_spdx_id, remove_prefix


@pytest.mark.parametrize("resource,doc_namespace,ext_namespace_mapping,expected",
                         [(URIRef("docNamespace#SPDXRef-Test"), "docNamespace", ("", Namespace("")), "SPDXRef-Test"),
                          (URIRef("docNamespaceSPDXRef-Test"), "docNamespace", ("", Namespace("")),
                           "docNamespaceSPDXRef-Test"),
                          (URIRef("differentNamespace#SPDXRef-Test"), "docNamespace",
                           ("extDoc", Namespace("differentNamespace#")), "extDoc:SPDXRef-Test"),
                          (None, "", ("", Namespace("")), None)])
def test_parse_spdx_id(resource, doc_namespace, ext_namespace_mapping, expected):
    graph = Graph()
    graph.bind(*ext_namespace_mapping)
    spdx_id = parse_spdx_id(resource, doc_namespace, graph)

    assert spdx_id == expected


@pytest.mark.parametrize("string,prefix,expected", [("prefixString", "prefix", "String"),
                                                    ("prefixString", "refix", "prefixString")])
def test_remove_prefix(string, prefix, expected):
    shorten_string = remove_prefix(string, prefix)

    assert expected == shorten_string
