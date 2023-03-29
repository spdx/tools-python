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
from rdflib import Graph, URIRef, RDF
from spdx.rdfschema.namespace import SPDX_NAMESPACE

from spdx.writer.rdf.external_document_ref_writer import add_external_document_ref_to_graph
from tests.spdx.fixtures import external_document_ref_fixture


def test_add_external_document_ref_to_graph():
    graph = Graph()
    external_document_ref = external_document_ref_fixture()

    add_external_document_ref_to_graph(external_document_ref, graph, URIRef("docNode"), "docNamespace")

    assert (URIRef("docNode"), SPDX_NAMESPACE.externalDocumentRef, URIRef("docNamespace#DocumentRef-external")) in graph
    assert (None, RDF.type, SPDX_NAMESPACE.ExternalDocumentRef) in graph
    assert (None, SPDX_NAMESPACE.checksum, None) in graph
    assert (None, RDF.type, SPDX_NAMESPACE.Checksum) in graph
    assert (None, SPDX_NAMESPACE.spdxDocument, URIRef(external_document_ref.document_uri)) in graph



