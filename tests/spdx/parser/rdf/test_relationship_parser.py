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
import os

from rdflib import Graph, RDF

from spdx.model.relationship import RelationshipType
from spdx.parser.rdf.relationship_parser import parse_relationship
from spdx.rdfschema.namespace import SPDX_NAMESPACE


def test_relationship_parser():
    graph = Graph().parse(os.path.join(os.path.dirname(__file__), "data/file_to_test_rdf_parser.rdf.xml"))
    parent_node = graph.value(predicate=RDF.type, object=SPDX_NAMESPACE.SpdxDocument)
    relationship_node = graph.value(subject=parent_node, predicate=SPDX_NAMESPACE.relationship)
    doc_namespace = "https://some.namespace"

    relationship = parse_relationship(relationship_node, graph, parent_node, doc_namespace)

    assert relationship.spdx_element_id == "SPDXRef-DOCUMENT"
    assert relationship.relationship_type == RelationshipType.DESCRIBES
    assert relationship.related_spdx_element_id == "SPDXRef-File"
    assert relationship.comment == "relationshipComment"
