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
from rdflib import URIRef, Graph, RDFS

from spdx.model.relationship import Relationship, RelationshipType
from spdx.parser.logger import Logger
from spdx.parser.parsing_functions import raise_parsing_error_if_logger_has_messages, construct_or_raise_parsing_error
from spdx.parser.rdf.graph_parsing_functions import parse_literal, parse_enum_value, \
    parse_literal_or_no_assertion_or_none, parse_spdx_id
from spdx.rdfschema.namespace import SPDX_NAMESPACE


def parse_relationship(relationship_node: URIRef, graph: Graph, parent_node: URIRef,
                       doc_namespace: str) -> Relationship:
    logger = Logger()
    spdx_element_id = parse_spdx_id(parent_node, doc_namespace, graph)

    relationship_type = parse_literal(
        logger, graph, relationship_node, SPDX_NAMESPACE.relationshipType,
        parsing_method=lambda x: parse_enum_value(x, RelationshipType, SPDX_NAMESPACE.relationshipType_))
    related_spdx_element = parse_literal_or_no_assertion_or_none(
        logger, graph, relationship_node, SPDX_NAMESPACE.relatedSpdxElement,
        parsing_method=lambda x: parse_spdx_id(x, doc_namespace, graph))

    comment = parse_literal(logger, graph, relationship_node, RDFS.comment)
    raise_parsing_error_if_logger_has_messages(logger, "Relationship")
    relationship = construct_or_raise_parsing_error(Relationship,
                                                    dict(spdx_element_id=spdx_element_id,
                                                         relationship_type=relationship_type,
                                                         related_spdx_element_id=related_spdx_element, comment=comment))

    return relationship
