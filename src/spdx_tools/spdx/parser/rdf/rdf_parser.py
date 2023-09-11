# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from beartype.typing import Any, Dict
from rdflib import RDF, Graph

from spdx_tools.spdx.model import Document, RelationshipType
from spdx_tools.spdx.parser.error import SPDXParsingError
from spdx_tools.spdx.parser.logger import Logger
from spdx_tools.spdx.parser.parsing_functions import (
    construct_or_raise_parsing_error,
    raise_parsing_error_if_logger_has_messages,
)
from spdx_tools.spdx.parser.rdf.annotation_parser import parse_annotation
from spdx_tools.spdx.parser.rdf.creation_info_parser import parse_creation_info
from spdx_tools.spdx.parser.rdf.extracted_licensing_info_parser import parse_extracted_licensing_info
from spdx_tools.spdx.parser.rdf.file_parser import parse_file
from spdx_tools.spdx.parser.rdf.graph_parsing_functions import get_correctly_typed_triples
from spdx_tools.spdx.parser.rdf.package_parser import parse_package
from spdx_tools.spdx.parser.rdf.relationship_parser import parse_implicit_relationship, parse_relationship
from spdx_tools.spdx.parser.rdf.snippet_parser import parse_snippet
from spdx_tools.spdx.rdfschema.namespace import SPDX_NAMESPACE


def parse_from_file(file_name: str, encoding: str = "utf-8") -> Document:
    graph = Graph()
    with open(file_name, encoding=encoding) as file:
        graph.parse(file, format="xml")

    document: Document = translate_graph_to_document(graph)
    return document


def translate_graph_to_document(graph: Graph) -> Document:
    parsed_fields: Dict[str, Any] = dict()
    logger = Logger()
    creation_info, doc_node = parse_creation_info(graph)

    parsed_fields["creation_info"] = creation_info

    for element, triple, parsing_method in [
        ("packages", (None, RDF.type, SPDX_NAMESPACE.Package), parse_package),
        ("files", (None, RDF.type, SPDX_NAMESPACE.File), parse_file),
        ("snippets", (None, RDF.type, SPDX_NAMESPACE.Snippet), parse_snippet),
    ]:
        elements = []
        for element_node, _, _ in get_correctly_typed_triples(logger, graph, *triple):
            try:
                elements.append(parsing_method(element_node, graph, creation_info.document_namespace))
            except SPDXParsingError as err:
                logger.extend(err.get_messages())
        parsed_fields[element] = elements

    for element, triple, parsing_method in [
        ("annotations", (None, SPDX_NAMESPACE.annotation, None), parse_annotation),
        ("relationships", (None, SPDX_NAMESPACE.relationship, None), parse_relationship),
    ]:
        elements = []
        for parent_node, _, element_node in graph.triples(triple):
            try:
                elements.append(parsing_method(element_node, graph, parent_node, creation_info.document_namespace))
            except SPDXParsingError as err:
                logger.extend(err.get_messages())
        parsed_fields[element] = elements

    for triple, relationship_type in [
        ((None, SPDX_NAMESPACE.hasFile, None), RelationshipType.CONTAINS),
        ((None, SPDX_NAMESPACE.describesPackage, None), RelationshipType.DESCRIBES),
    ]:
        for parent_node, _, element_node in get_correctly_typed_triples(logger, graph, *triple):
            try:
                relationship = parse_implicit_relationship(
                    parent_node, relationship_type, element_node, graph, creation_info.document_namespace
                )
                if relationship not in parsed_fields["relationships"]:
                    parsed_fields["relationships"].append(relationship)

            except SPDXParsingError as err:
                logger.extend(err.get_messages())

    extracted_licensing_infos = []
    for _, _, extracted_licensing_info_node in get_correctly_typed_triples(
        logger, graph, None, SPDX_NAMESPACE.hasExtractedLicensingInfo
    ):
        try:
            extracted_licensing_infos.append(
                parse_extracted_licensing_info(extracted_licensing_info_node, graph, creation_info.document_namespace)
            )
        except SPDXParsingError as err:
            logger.extend(err.get_messages())
    parsed_fields["extracted_licensing_info"] = extracted_licensing_infos

    raise_parsing_error_if_logger_has_messages(logger)
    document = construct_or_raise_parsing_error(Document, parsed_fields)

    return document
