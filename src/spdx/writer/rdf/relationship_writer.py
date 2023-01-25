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
from rdflib import Graph, BNode, RDF, URIRef

from spdx.model.relationship import Relationship
from spdx.writer.casing_tools import snake_case_to_camel_case
from spdx.writer.rdf.writer_utils import spdx_namespace


def add_relationship_info_to_graph(relationship: Relationship, graph: Graph, doc_namespace: str):
    relationship_node = BNode()
    graph.add((relationship_node, RDF.type, spdx_namespace.Relationship))
    graph.add((relationship_node, spdx_namespace.relationshipType,
               spdx_namespace[f"relationshipType_{snake_case_to_camel_case(relationship.relationship_type.name)}"]))
    graph.add((relationship_node, spdx_namespace.relatedSpdxElement,
               URIRef(f"{doc_namespace}#{relationship.related_spdx_element_id}")))

    relationship_resource = URIRef(f"{doc_namespace}#{relationship.spdx_element_id}")
    graph.add((relationship_resource, spdx_namespace.relationship, relationship_node))