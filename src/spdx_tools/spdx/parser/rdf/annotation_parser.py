# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from rdflib import RDFS, BNode, Graph, URIRef

from spdx_tools.spdx.datetime_conversions import datetime_from_str
from spdx_tools.spdx.model import Annotation, AnnotationType
from spdx_tools.spdx.parser.actor_parser import ActorParser
from spdx_tools.spdx.parser.logger import Logger
from spdx_tools.spdx.parser.parsing_functions import (
    construct_or_raise_parsing_error,
    raise_parsing_error_if_logger_has_messages,
)
from spdx_tools.spdx.parser.rdf.graph_parsing_functions import parse_enum_value, parse_literal, parse_spdx_id
from spdx_tools.spdx.rdfschema.namespace import SPDX_NAMESPACE


def parse_annotation(annotation_node: BNode, graph: Graph, parent_node: URIRef, doc_namespace: str) -> Annotation:
    logger = Logger()
    spdx_id = parse_spdx_id(parent_node, doc_namespace, graph)
    annotator = parse_literal(
        logger, graph, annotation_node, SPDX_NAMESPACE.annotator, parsing_method=ActorParser.parse_actor
    )
    annotation_type = parse_literal(
        logger,
        graph,
        annotation_node,
        SPDX_NAMESPACE.annotationType,
        parsing_method=lambda x: parse_enum_value(x, AnnotationType, SPDX_NAMESPACE.annotationType_),
    )
    annotation_date = parse_literal(
        logger, graph, annotation_node, SPDX_NAMESPACE.annotationDate, parsing_method=datetime_from_str
    )
    annotation_comment = parse_literal(logger, graph, annotation_node, RDFS.comment)

    raise_parsing_error_if_logger_has_messages(logger, "Annotation")
    annotation = construct_or_raise_parsing_error(
        Annotation,
        dict(
            spdx_id=spdx_id,
            annotation_type=annotation_type,
            annotator=annotator,
            annotation_date=annotation_date,
            annotation_comment=annotation_comment,
        ),
    )

    return annotation
