# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import pytest
from rdflib import RDF, RDFS, Graph, Literal, URIRef

from spdx_tools.spdx.rdfschema.namespace import LICENSE_NAMESPACE, POINTER_NAMESPACE, SPDX_NAMESPACE
from spdx_tools.spdx.writer.rdf.snippet_writer import add_range_to_graph, add_snippet_to_graph
from tests.spdx.fixtures import snippet_fixture


def test_add_snippet_to_graph():
    graph = Graph()
    snippet = snippet_fixture()

    add_snippet_to_graph(snippet, graph, "docNamespace", {})

    assert (URIRef("docNamespace#SPDXRef-Snippet"), RDF.type, SPDX_NAMESPACE.Snippet) in graph
    assert (None, SPDX_NAMESPACE.snippetFromFile, URIRef(f"docNamespace#{snippet.file_spdx_id}")) in graph
    assert (None, SPDX_NAMESPACE.licenseConcluded, None) in graph
    assert (None, SPDX_NAMESPACE.licenseInfoInSnippet, LICENSE_NAMESPACE.MIT) in graph
    assert (None, SPDX_NAMESPACE.licenseInfoInSnippet, LICENSE_NAMESPACE["GPL-2.0-only"]) in graph
    assert (None, SPDX_NAMESPACE.licenseInfoInSnippet, SPDX_NAMESPACE.none) in graph
    assert (None, SPDX_NAMESPACE.licenseComments, Literal(snippet.license_comment)) in graph
    assert (None, SPDX_NAMESPACE.copyrightText, Literal(snippet.copyright_text)) in graph
    assert (None, SPDX_NAMESPACE.name, Literal(snippet.name)) in graph
    assert (None, SPDX_NAMESPACE.attributionText, Literal(snippet.attribution_texts[0])) in graph
    assert (None, RDFS.comment, Literal(snippet.comment)) in graph


@pytest.mark.parametrize(
    "range,pointer,predicate",
    [
        ((5, 190), POINTER_NAMESPACE.ByteOffsetPointer, POINTER_NAMESPACE.offset),
        ((1, 3), POINTER_NAMESPACE.LineCharPointer, POINTER_NAMESPACE.lineNumber),
    ],
)
def test_add_ranges_to_graph(range, pointer, predicate):
    graph = Graph()
    add_range_to_graph(range, graph, URIRef("snippetNode"), URIRef("docNamespace#SPDXRef-File"), pointer)

    assert (URIRef("snippetNode"), SPDX_NAMESPACE.range, None) in graph
    assert (None, POINTER_NAMESPACE.startPointer, None) in graph
    assert (None, POINTER_NAMESPACE.endPointer, None) in graph
    assert (None, POINTER_NAMESPACE.reference, URIRef("docNamespace#SPDXRef-File")) in graph
    assert (None, predicate, Literal(range[0])) in graph
    assert (None, predicate, Literal(range[1])) in graph
