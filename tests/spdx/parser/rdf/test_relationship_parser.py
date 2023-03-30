# SPDX-FileCopyrightText: 2023 spdx contributors

# SPDX-License-Identifier: Apache-2.0
import os

from rdflib import RDF, Graph

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
