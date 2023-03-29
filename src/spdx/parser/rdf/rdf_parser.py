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
from rdflib import Graph, RDF

from spdx.model.document import Document
from spdx.parser.error import SPDXParsingError
from spdx.parser.logger import Logger
from spdx.parser.parsing_functions import construct_or_raise_parsing_error, raise_parsing_error_if_logger_has_messages
from spdx.parser.rdf.annotation_parser import parse_annotation
from spdx.parser.rdf.creation_info_parser import parse_creation_info
from spdx.parser.rdf.extracted_licensing_info_parser import parse_extracted_licensing_info
from spdx.parser.rdf.file_parser import parse_file
from spdx.parser.rdf.package_parser import parse_package
from spdx.parser.rdf.relationship_parser import parse_relationship
from spdx.parser.rdf.snippet_parser import parse_snippet
from spdx.rdfschema.namespace import SPDX_NAMESPACE


def parse_from_file(file_name: str) -> Document:
    graph = Graph()
    with open(file_name) as file:
        graph.parse(file, format="xml")

    document: Document = translate_graph_to_document(graph)
    return document


def translate_graph_to_document(graph: Graph) -> Document:
    parsed_fields = dict()
    logger = Logger()
    try:
        creation_info, doc_node = parse_creation_info(graph)
    except SPDXParsingError as err:
        logger.extend(err.get_messages())
        creation_info = None

    parsed_fields["creation_info"] = creation_info

    for element, triple, parsing_method in [("packages", (None, RDF.type, SPDX_NAMESPACE.Package), parse_package),
                                            ("files", (None, RDF.type, SPDX_NAMESPACE.File), parse_file),
                                            ("snippets", (None, RDF.type, SPDX_NAMESPACE.Snippet), parse_snippet)]:
        elements = []
        for (element_node, _, _) in graph.triples(triple):
            try:
                elements.append(parsing_method(element_node, graph, creation_info.document_namespace))
            except SPDXParsingError as err:
                logger.extend(err.get_messages())
        parsed_fields[element] = elements

    for element, triple, parsing_method in [("annotations", (None, SPDX_NAMESPACE.annotation, None), parse_annotation),
                                            ("relationships", (None, SPDX_NAMESPACE.relationship, None),
                                             parse_relationship)]:
        elements = []
        for (parent_node, _, element_node) in graph.triples(triple):
            try:
                elements.append(parsing_method(element_node, graph, parent_node, creation_info.document_namespace))
            except SPDXParsingError as err:
                logger.extend(err.get_messages())
        parsed_fields[element] = elements

    extracted_licensing_infos = []
    for (_, _, extracted_licensing_info_node) in graph.triples((None, SPDX_NAMESPACE.hasExtractedLicensingInfo, None)):
        try:
            extracted_licensing_infos.append(parse_extracted_licensing_info(extracted_licensing_info_node, graph))
        except SPDXParsingError as err:
            logger.extend(err.get_messages())
    parsed_fields["extracted_licensing_info"] = extracted_licensing_infos

    raise_parsing_error_if_logger_has_messages(logger)
    document = construct_or_raise_parsing_error(Document, parsed_fields)

    return document
