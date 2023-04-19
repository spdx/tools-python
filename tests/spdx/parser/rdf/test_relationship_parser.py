# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import os

import pytest
from rdflib import RDF, Graph, URIRef

from spdx_tools.spdx.constants import DOCUMENT_SPDX_ID
from spdx_tools.spdx.model import RelationshipType
from spdx_tools.spdx.parser.rdf.relationship_parser import parse_implicit_relationship, parse_relationship
from spdx_tools.spdx.rdfschema.namespace import SPDX_NAMESPACE


def test_relationship_parser():
    graph = Graph().parse(os.path.join(os.path.dirname(__file__), "data/file_to_test_rdf_parser.rdf.xml"))
    parent_node = graph.value(predicate=RDF.type, object=SPDX_NAMESPACE.SpdxDocument)
    relationship_node = graph.value(subject=parent_node, predicate=SPDX_NAMESPACE.relationship)
    doc_namespace = "https://some.namespace"
    assert isinstance(parent_node, URIRef)

    relationship = parse_relationship(relationship_node, graph, parent_node, doc_namespace)

    assert relationship.spdx_element_id == DOCUMENT_SPDX_ID
    assert relationship.relationship_type == RelationshipType.DESCRIBES
    assert relationship.related_spdx_element_id == "SPDXRef-File"
    assert relationship.comment == "relationshipComment"


@pytest.mark.parametrize(
    "parent_node, predicate, spdx_element_id, relationship_type, related_spdx_element_id",
    [
        (
            SPDX_NAMESPACE.SpdxDocument,
            SPDX_NAMESPACE.describesPackage,
            DOCUMENT_SPDX_ID,
            RelationshipType.DESCRIBES,
            "SPDXRef-Package",
        ),
        (SPDX_NAMESPACE.Package, SPDX_NAMESPACE.hasFile, "SPDXRef-Package", RelationshipType.CONTAINS, "SPDXRef-File"),
    ],
)
def test_parse_implicit_relationship(
    parent_node, predicate, spdx_element_id, relationship_type, related_spdx_element_id
):
    graph = Graph().parse(os.path.join(os.path.dirname(__file__), "data/file_to_test_rdf_parser.rdf.xml"))
    parent_node = graph.value(predicate=RDF.type, object=parent_node)
    relationship_node = graph.value(subject=parent_node, predicate=predicate)
    assert isinstance(relationship_node, URIRef)
    assert isinstance(parent_node, URIRef)

    doc_namespace = "https://some.namespace"

    relationship = parse_implicit_relationship(parent_node, relationship_type, relationship_node, graph, doc_namespace)

    assert relationship.spdx_element_id == spdx_element_id
    assert relationship.relationship_type == relationship_type
    assert relationship.related_spdx_element_id == related_spdx_element_id
