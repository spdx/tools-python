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
from typing import Dict

from rdflib import Graph, BNode, RDF, URIRef

from spdx.model.relationship import Relationship
from spdx.model.spdx_no_assertion import SpdxNoAssertion
from spdx.model.spdx_none import SpdxNone
from spdx.writer.casing_tools import snake_case_to_camel_case
from spdx.writer.rdf.writer_utils import spdx_namespace, add_namespace_to_spdx_id


def add_relationship_info_to_graph(relationship: Relationship, graph: Graph, doc_namespace: str,
                                   external_doc_namespaces: Dict[str, str]):
    relationship_node = BNode()
    graph.add((relationship_node, RDF.type, spdx_namespace.Relationship))
    graph.add((relationship_node, spdx_namespace.relationshipType,
               spdx_namespace[f"relationshipType_{snake_case_to_camel_case(relationship.relationship_type.name)}"]))
    if isinstance(relationship.related_spdx_element_id, SpdxNone):
        graph.add((relationship_node, spdx_namespace.relatedSpdxElement, spdx_namespace.none))
    elif isinstance(relationship.related_spdx_element_id, SpdxNoAssertion):
        graph.add((relationship_node, spdx_namespace.relatedSpdxElement, spdx_namespace.noassertion))
    else:
        graph.add((relationship_node, spdx_namespace.relatedSpdxElement,
                   URIRef(add_namespace_to_spdx_id(relationship.related_spdx_element_id, doc_namespace,
                                                   external_doc_namespaces))))

    relationship_resource = URIRef(
        add_namespace_to_spdx_id(relationship.spdx_element_id, doc_namespace, external_doc_namespaces))
    graph.add((relationship_resource, spdx_namespace.relationship, relationship_node))
