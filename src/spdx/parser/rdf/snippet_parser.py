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
from typing import Tuple, Optional

from rdflib import Graph, RDF, RDFS
from rdflib.term import URIRef, Node

from spdx.model.snippet import Snippet
from spdx.parser.logger import Logger
from spdx.parser.parsing_functions import construct_or_raise_parsing_error, raise_parsing_error_if_logger_has_messages
from spdx.parser.rdf.graph_parsing_functions import parse_literal, parse_spdx_id, parse_literal_or_no_assertion_or_none, \
    get_correct_typed_value
from spdx.parser.rdf.license_expression_parser import parse_license_expression
from spdx.rdfschema.namespace import SPDX_NAMESPACE, POINTER_NAMESPACE


def parse_snippet(snippet_node: URIRef, graph: Graph, doc_namespace: str) -> Snippet:
    logger = Logger()
    spdx_id = parse_spdx_id(snippet_node, doc_namespace, graph)
    file_spdx_id_uri = graph.value(subject=snippet_node, predicate=SPDX_NAMESPACE.snippetFromFile)
    file_spdx_id = parse_spdx_id(file_spdx_id_uri, doc_namespace, graph)
    byte_range = parse_ranges(snippet_node, graph, POINTER_NAMESPACE.ByteOffsetPointer, POINTER_NAMESPACE.offset)
    line_range = parse_ranges(snippet_node, graph, POINTER_NAMESPACE.LineCharPointer, POINTER_NAMESPACE.lineNumber)
    license_concluded = parse_literal_or_no_assertion_or_none(logger, graph, snippet_node,
                                                              SPDX_NAMESPACE.licenseConcluded,
                                                              parsing_method=lambda x: parse_license_expression(x,
                                                                                                                graph))
    license_info_in_snippet = []
    for (_, _, license_info_in_snippet_node) in graph.triples(
        (snippet_node, SPDX_NAMESPACE.licenseInfoInSnippet, None)):
        license_info_in_snippet.append(
            get_correct_typed_value(logger, license_info_in_snippet_node, lambda x: parse_license_expression(x, graph)))
    license_comment = parse_literal(logger, graph, snippet_node, SPDX_NAMESPACE.licenseComments)
    copyright_text = parse_literal_or_no_assertion_or_none(logger, graph, snippet_node, SPDX_NAMESPACE.copyrightText,
                                                           parsing_method=str)
    comment = parse_literal(logger, graph, snippet_node, RDFS.comment)
    name = parse_literal(logger, graph, snippet_node, SPDX_NAMESPACE.name)
    attribution_texts = []
    for (_, _, attribution_text_literal) in graph.triples((snippet_node, SPDX_NAMESPACE.attributionText, None)):
        attribution_texts.append(attribution_text_literal.toPython())

    raise_parsing_error_if_logger_has_messages(logger, "Snippet")
    snippet = construct_or_raise_parsing_error(Snippet,
                                               dict(spdx_id=spdx_id, file_spdx_id=file_spdx_id, byte_range=byte_range,
                                                    line_range=line_range, license_concluded=license_concluded,
                                                    license_info_in_snippet=license_info_in_snippet,
                                                    license_comment=license_comment,
                                                    copyright_text=copyright_text, comment=comment, name=name,
                                                    attribution_texts=attribution_texts))
    return snippet


def parse_ranges(snippet_node: URIRef, graph: Graph, pointer: Node, member: Node) -> Tuple[int, int]:
    start_range = None
    end_range = None
    for (_, _, start_end_pointer) in graph.triples((snippet_node, SPDX_NAMESPACE.range, None)):
        for (_, _, pointer_node) in graph.triples((start_end_pointer, POINTER_NAMESPACE.startPointer, None)):
            for (typed_pointer_node, _, _) in graph.triples((pointer_node, RDF.type, pointer)):
                start_range = parse_range_value(graph, typed_pointer_node, member)
        for (_, _, pointer_node) in graph.triples((start_end_pointer, POINTER_NAMESPACE.endPointer, None)):
            for (typed_pointer_node, _, _) in graph.triples((pointer_node, RDF.type, pointer)):
                end_range = parse_range_value(graph, typed_pointer_node, member)
    return start_range, end_range


def parse_range_value(graph: Graph, pointer_node: Node, predicate: Node) -> Optional[int]:
    value = graph.value(pointer_node, predicate)
    if value:
        value = int(value)
    return value
