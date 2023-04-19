# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from rdflib import RDFS, Graph, Literal, URIRef

from spdx_tools.spdx.constants import DOCUMENT_SPDX_ID
from spdx_tools.spdx.rdfschema.namespace import SPDX_NAMESPACE
from spdx_tools.spdx.writer.rdf.relationship_writer import add_relationship_to_graph
from tests.spdx.fixtures import relationship_fixture


def test_add_relationship_to_graph():
    relationship = relationship_fixture()
    graph = Graph()
    add_relationship_to_graph(relationship, graph, "docNamespace", {})

    assert (URIRef(f"docNamespace#{DOCUMENT_SPDX_ID}"), SPDX_NAMESPACE.relationship, None) in graph
    assert (None, SPDX_NAMESPACE.relationshipType, SPDX_NAMESPACE.relationshipType_describes) in graph
    assert (None, SPDX_NAMESPACE.relatedSpdxElement, URIRef("docNamespace#SPDXRef-File")) in graph
    assert (None, RDFS.comment, Literal(relationship.comment)) in graph
