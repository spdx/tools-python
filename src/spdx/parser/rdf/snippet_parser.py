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
from typing import Tuple, Optional, Dict

from rdflib import Graph, RDF, RDFS
from rdflib.exceptions import UniquenessError
from rdflib.term import URIRef, Node
from spdx.parser.error import SPDXParsingError

from spdx.model.snippet import Snippet
from spdx.parser.logger import Logger
from spdx.parser.parsing_functions import construct_or_raise_parsing_error, raise_parsing_error_if_logger_has_messages
from spdx.parser.rdf.graph_parsing_functions import parse_literal, parse_spdx_id, parse_literal_or_no_assertion_or_none, \
    get_correctly_typed_value, apply_parsing_method_or_log_error
from spdx.parser.rdf.license_expression_parser import parse_license_expression
from spdx.rdfschema.namespace import SPDX_NAMESPACE, POINTER_NAMESPACE


def parse_snippet(snippet_node: URIRef, graph: Graph, doc_namespace: str) -> Snippet:
    logger = Logger()
    spdx_id = parse_spdx_id(snippet_node, doc_namespace, graph)
    file_spdx_id_uri = graph.value(subject=snippet_node, predicate=SPDX_NAMESPACE.snippetFromFile)
    file_spdx_id = parse_spdx_id(file_spdx_id_uri, doc_namespace, graph)
    byte_range = None
    line_range = None
    for (_, _, start_end_pointer) in graph.triples((snippet_node, SPDX_NAMESPACE.range, None)):
        parsed_range = apply_parsing_method_or_log_error(logger, start_end_pointer,
                                                         parsing_method=lambda x: parse_ranges(x, graph))
        byte_range, line_range = set_range_or_log_error(byte_range, line_range, logger, parsed_range)

    license_concluded = parse_literal_or_no_assertion_or_none(
        logger, graph, snippet_node, SPDX_NAMESPACE.licenseConcluded,
        parsing_method=lambda x: parse_license_expression(x, graph, doc_namespace))
    license_info_in_snippet = []
    for (_, _, license_info_in_snippet_node) in graph.triples(
        (snippet_node, SPDX_NAMESPACE.licenseInfoInSnippet, None)):
        license_info_in_snippet.append(
            get_correctly_typed_value(logger, license_info_in_snippet_node,
                                      lambda x: parse_license_expression(x, graph, doc_namespace)))
    license_comment = parse_literal(logger, graph, snippet_node, SPDX_NAMESPACE.licenseComments)
    copyright_text = parse_literal_or_no_assertion_or_none(logger, graph, snippet_node, SPDX_NAMESPACE.copyrightText)
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


def set_range_or_log_error(
    byte_range: Optional[Tuple[int, int]], line_range: Optional[Tuple[int, int]], logger: Logger,
    parsed_range: Dict[str, Tuple[int, int]]) -> Tuple[Optional[Tuple[int, int]], Optional[Tuple[int, int]]]:
    if not parsed_range:
        return byte_range, line_range
    if "ByteOffsetPointer" in parsed_range.keys() and not byte_range:
        byte_range = parsed_range["ByteOffsetPointer"]
    elif "ByteOffsetPointer" in parsed_range.keys() and byte_range:
        logger.append("Multiple ByteOffsetPointer found.")
    elif "LineCharPointer" in parsed_range.keys() and not line_range:
        line_range = parsed_range["LineCharPointer"]
    elif "LineCharPointer" in parsed_range.keys() and line_range:
        logger.append("Multiple LineCharPointer found.")
    return byte_range, line_range


def parse_ranges(start_end_pointer: URIRef, graph: Graph) -> Dict[str, Tuple[int, int]]:
    range_values = dict()
    start_pointer_type, start_pointer_node = get_pointer_type(graph, POINTER_NAMESPACE.startPointer, start_end_pointer)
    end_pointer_type, end_pointer_node = get_pointer_type(graph, POINTER_NAMESPACE.endPointer, start_end_pointer)

    if start_pointer_type != end_pointer_type:
        raise SPDXParsingError([f"Types of startPointer and endPointer don't match"])

    range_values["startPointer"] = parse_range_value(graph, start_pointer_node, POINTER_MATCHING[start_pointer_type])
    range_values["endPointer"] = parse_range_value(graph, end_pointer_node, POINTER_MATCHING[end_pointer_type])

    return {str(start_pointer_type.fragment): (
        range_values["startPointer"], range_values["endPointer"])}


def get_pointer_type(graph: Graph, pointer: URIRef, start_end_pointer: URIRef) -> Tuple[URIRef, URIRef]:
    try:
        pointer_node = graph.value(start_end_pointer, pointer, any=False)
    except UniquenessError:
        raise SPDXParsingError([f"Multiple values for {pointer.fragment}"])
    if not pointer_node:
        raise SPDXParsingError([f"Couldn't find pointer of type {pointer.fragment}."])
    pointer_type = graph.value(pointer_node, RDF.type)
    return pointer_type, pointer_node


POINTER_MATCHING = {
    POINTER_NAMESPACE.ByteOffsetPointer: POINTER_NAMESPACE.offset,
    POINTER_NAMESPACE.LineCharPointer: POINTER_NAMESPACE.lineNumber}


def parse_range_value(graph: Graph, pointer_node: Node, predicate: URIRef) -> Optional[int]:
    try:
        value = graph.value(pointer_node, predicate, any=False)
    except UniquenessError:
        raise SPDXParsingError([f"Multiple values for {predicate.fragment} found."])
    if value:
        value = int(value)
    return value
