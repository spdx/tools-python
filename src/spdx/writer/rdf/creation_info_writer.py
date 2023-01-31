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
from rdflib import Graph, BNode, RDF, Literal, RDFS, URIRef

from spdx.datetime_conversions import datetime_to_iso_string
from spdx.model.document import CreationInfo
from spdx.writer.rdf.external_document_ref_writer import add_external_document_ref_to_graph
from spdx.writer.rdf.writer_utils import add_optional_literal
from spdx.rdfschema.namespace import SPDX_NAMESPACE, LICENSE_NAMESPACE


def add_creation_info_to_graph(creation_info: CreationInfo, graph: Graph):
    doc_node = URIRef(f"{creation_info.document_namespace}#{creation_info.spdx_id}")
    graph.add((doc_node, RDF.type, SPDX_NAMESPACE.SpdxDocument))
    graph.add((doc_node, SPDX_NAMESPACE.specVersion, Literal(creation_info.spdx_version)))
    graph.add((doc_node, SPDX_NAMESPACE.dataLicense, LICENSE_NAMESPACE[creation_info.data_license]))
    graph.add((doc_node, SPDX_NAMESPACE.name, Literal(creation_info.name)))
    add_optional_literal(creation_info.document_comment, graph, doc_node, RDFS.comment)

    creation_info_node = BNode()
    graph.add((creation_info_node, RDF.type, SPDX_NAMESPACE.CreationInfo))

    graph.add((creation_info_node, SPDX_NAMESPACE.created, Literal(datetime_to_iso_string(creation_info.created))))

    for creator in creation_info.creators:
        graph.add((creation_info_node, SPDX_NAMESPACE.creator, Literal(creator.to_serialized_string())))

    add_optional_literal(creation_info.license_list_version, graph, creation_info_node,
                         SPDX_NAMESPACE.licenseListVersion)
    add_optional_literal(creation_info.creator_comment, graph, creation_info_node, RDFS.comment)

    graph.add((doc_node, SPDX_NAMESPACE.creationInfo, creation_info_node))

    for external_document_ref in creation_info.external_document_refs:
        add_external_document_ref_to_graph(external_document_ref, graph, doc_node, creation_info.document_namespace)

    return doc_node
