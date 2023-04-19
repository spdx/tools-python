# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import pytest
from rdflib import Graph, Namespace, URIRef

from spdx_tools.spdx.parser.rdf.graph_parsing_functions import parse_spdx_id, remove_prefix


@pytest.mark.parametrize(
    "resource,doc_namespace,ext_namespace_mapping,expected",
    [
        (URIRef("docNamespace#SPDXRef-Test"), "docNamespace", ("", Namespace("")), "SPDXRef-Test"),
        (URIRef("docNamespaceSPDXRef-Test"), "docNamespace", ("", Namespace("")), "docNamespaceSPDXRef-Test"),
        (
            URIRef("differentNamespace#SPDXRef-Test"),
            "docNamespace",
            ("extDoc", Namespace("differentNamespace#")),
            "extDoc:SPDXRef-Test",
        ),
        (None, "", ("", Namespace("")), None),
    ],
)
def test_parse_spdx_id(resource, doc_namespace, ext_namespace_mapping, expected):
    graph = Graph()
    graph.bind(*ext_namespace_mapping)
    spdx_id = parse_spdx_id(resource, doc_namespace, graph)

    assert spdx_id == expected


@pytest.mark.parametrize(
    "string,prefix,expected", [("prefixString", "prefix", "String"), ("prefixString", "refix", "prefixString")]
)
def test_remove_prefix(string, prefix, expected):
    shorten_string = remove_prefix(string, prefix)

    assert expected == shorten_string
