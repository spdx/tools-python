# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from typing import Dict

from rdflib import RDF, RDFS, BNode, Graph, Literal, URIRef

from spdx.casing_tools import snake_case_to_camel_case
from spdx.model.relationship import Relationship
from spdx.model.spdx_no_assertion import SpdxNoAssertion
from spdx.model.spdx_none import SpdxNone
from spdx.rdfschema.namespace import SPDX_NAMESPACE
from spdx.writer.rdf.writer_utils import add_namespace_to_spdx_id


def add_relationship_to_graph(
    relationship: Relationship, graph: Graph, doc_namespace: str, external_doc_ref_to_namespace: Dict[str, str]
):
    relationship_node = BNode()
    graph.add((relationship_node, RDF.type, SPDX_NAMESPACE.Relationship))
    graph.add(
        (
            relationship_node,
            SPDX_NAMESPACE.relationshipType,
            SPDX_NAMESPACE[f"relationshipType_{snake_case_to_camel_case(relationship.relationship_type.name)}"],
        )
    )
    if isinstance(relationship.related_spdx_element_id, SpdxNone):
        graph.add((relationship_node, SPDX_NAMESPACE.relatedSpdxElement, SPDX_NAMESPACE.none))
    elif isinstance(relationship.related_spdx_element_id, SpdxNoAssertion):
        graph.add((relationship_node, SPDX_NAMESPACE.relatedSpdxElement, SPDX_NAMESPACE.noassertion))
    else:
        graph.add(
            (
                relationship_node,
                SPDX_NAMESPACE.relatedSpdxElement,
                URIRef(
                    add_namespace_to_spdx_id(
                        relationship.related_spdx_element_id, doc_namespace, external_doc_ref_to_namespace
                    )
                ),
            )
        )
    graph.add((relationship_node, RDFS.comment, Literal(relationship.comment)))
    relationship_resource = URIRef(
        add_namespace_to_spdx_id(relationship.spdx_element_id, doc_namespace, external_doc_ref_to_namespace)
    )
    graph.add((relationship_resource, SPDX_NAMESPACE.relationship, relationship_node))
