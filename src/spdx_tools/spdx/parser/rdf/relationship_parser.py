# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from rdflib import RDFS, Graph, URIRef
from rdflib.term import Node

from spdx_tools.spdx.model import Relationship, RelationshipType
from spdx_tools.spdx.parser.logger import Logger
from spdx_tools.spdx.parser.parsing_functions import (
    construct_or_raise_parsing_error,
    raise_parsing_error_if_logger_has_messages,
)
from spdx_tools.spdx.parser.rdf.graph_parsing_functions import (
    parse_enum_value,
    parse_literal,
    parse_literal_or_no_assertion_or_none,
    parse_spdx_id,
)
from spdx_tools.spdx.rdfschema.namespace import SPDX_NAMESPACE


def parse_relationship(relationship_node: Node, graph: Graph, parent_node: URIRef, doc_namespace: str) -> Relationship:
    logger = Logger()
    spdx_element_id = parse_spdx_id(parent_node, doc_namespace, graph)

    relationship_type = parse_literal(
        logger,
        graph,
        relationship_node,
        SPDX_NAMESPACE.relationshipType,
        parsing_method=lambda x: parse_enum_value(x, RelationshipType, SPDX_NAMESPACE.relationshipType_),
    )
    related_spdx_element = parse_literal_or_no_assertion_or_none(
        logger,
        graph,
        relationship_node,
        SPDX_NAMESPACE.relatedSpdxElement,
        parsing_method=lambda x: parse_spdx_id(x, doc_namespace, graph),
    )

    comment = parse_literal(logger, graph, relationship_node, RDFS.comment)
    raise_parsing_error_if_logger_has_messages(logger, "Relationship")
    relationship = construct_or_raise_parsing_error(
        Relationship,
        dict(
            spdx_element_id=spdx_element_id,
            relationship_type=relationship_type,
            related_spdx_element_id=related_spdx_element,
            comment=comment,
        ),
    )

    return relationship


def parse_implicit_relationship(
    spdx_element_node: URIRef,
    relationship_type: RelationshipType,
    related_spdx_element_node: URIRef,
    graph: Graph,
    doc_namespace: str,
) -> Relationship:
    spdx_element_id = parse_spdx_id(spdx_element_node, doc_namespace, graph)
    related_spdx_element_id = parse_spdx_id(related_spdx_element_node, doc_namespace, graph)
    relationship = construct_or_raise_parsing_error(
        Relationship,
        dict(
            spdx_element_id=spdx_element_id,
            relationship_type=relationship_type,
            related_spdx_element_id=related_spdx_element_id,
        ),
    )
    return relationship
