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

from spdx.model.external_document_ref import ExternalDocumentRef
from spdx.writer.rdf.checksum_writer import add_checksum_to_graph
from spdx.rdfschema.namespace import SPDX_NAMESPACE


def add_external_document_ref_to_graph(external_document_ref: ExternalDocumentRef, graph: Graph, doc_node: URIRef,
                                       doc_namespace: str):
    external_document_ref_resource = URIRef(f"{doc_namespace}#{external_document_ref.document_ref_id}")
    graph.add((external_document_ref_resource, RDF.type, SPDX_NAMESPACE.ExternalDocumentRef))
    graph.add((external_document_ref_resource, SPDX_NAMESPACE.spdxDocument, URIRef(external_document_ref.document_uri)))
    add_checksum_to_graph(external_document_ref.checksum, graph, external_document_ref_resource)

    graph.add((doc_node, SPDX_NAMESPACE.externalDocumentRef, external_document_ref_resource))
