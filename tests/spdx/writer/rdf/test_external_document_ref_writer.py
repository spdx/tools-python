# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from rdflib import RDF, Graph, URIRef

from spdx_tools.spdx.rdfschema.namespace import SPDX_NAMESPACE
from spdx_tools.spdx.writer.rdf.external_document_ref_writer import add_external_document_ref_to_graph
from tests.spdx.fixtures import external_document_ref_fixture


def test_add_external_document_ref_to_graph():
    graph = Graph()
    external_document_ref = external_document_ref_fixture()

    add_external_document_ref_to_graph(external_document_ref, graph, URIRef("docNode"), "docNamespace")

    assert (
        URIRef("docNode"),
        SPDX_NAMESPACE.externalDocumentRef,
        URIRef("docNamespace#DocumentRef-external"),
    ) in graph
    assert (None, RDF.type, SPDX_NAMESPACE.ExternalDocumentRef) in graph
    assert (None, SPDX_NAMESPACE.checksum, None) in graph
    assert (None, RDF.type, SPDX_NAMESPACE.Checksum) in graph
    assert (None, SPDX_NAMESPACE.spdxDocument, URIRef(external_document_ref.document_uri)) in graph
