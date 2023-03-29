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

from spdx.datetime_conversions import datetime_from_str
from spdx.model.annotation import Annotation, AnnotationType
from spdx.parser.actor_parser import ActorParser
from spdx.parser.logger import Logger
from spdx.parser.parsing_functions import raise_parsing_error_if_logger_has_messages, construct_or_raise_parsing_error
from spdx.parser.rdf.graph_parsing_functions import parse_literal, parse_spdx_id, parse_enum_value
from spdx.rdfschema.namespace import SPDX_NAMESPACE


def parse_annotation(annotation_node: URIRef, graph: Graph, parent_node: URIRef, doc_namespace: str) -> Annotation:
    logger = Logger()
    spdx_id = parse_spdx_id(parent_node, doc_namespace, graph)
    annotator = parse_literal(logger, graph, annotation_node, SPDX_NAMESPACE.annotator,
                              parsing_method=ActorParser.parse_actor)
    annotation_type = parse_literal(logger, graph, annotation_node, SPDX_NAMESPACE.annotationType,
                                    parsing_method=lambda x: parse_enum_value(x, AnnotationType,
                                                                              SPDX_NAMESPACE.annotationType_))
    annotation_date = parse_literal(logger, graph, annotation_node, SPDX_NAMESPACE.annotationDate,
                                    parsing_method=datetime_from_str)
    annotation_comment = parse_literal(logger, graph, annotation_node, RDFS.comment)

    raise_parsing_error_if_logger_has_messages(logger, "Annotation")
    annotation = construct_or_raise_parsing_error(Annotation, dict(spdx_id=spdx_id, annotation_type=annotation_type,
                                                                   annotator=annotator, annotation_date=annotation_date,
                                                                   annotation_comment=annotation_comment))

    return annotation
