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
from spdx.parser.rdf.creation_info_parser import parse_creation_info
from spdx.parser.rdf.snippet_parser import parse_snippet
from spdx.rdfschema.namespace import SPDX_NAMESPACE


def parse_from_file(file_name: str) -> Document:
    graph = Graph()
    with open(file_name) as file:
        graph.parse(file, format="xml")

    document: Document = translate_graph_to_document(graph)
    return document


def translate_graph_to_document(graph: Graph) -> Document:
    logger = Logger()
    try:
        creation_info, doc_node = parse_creation_info(graph)
    except SPDXParsingError as err:
        logger.extend(err.get_messages())
        creation_info = None

    snippets = []
    for (snippet_node, _, _) in graph.triples((None, RDF.type, SPDX_NAMESPACE.Snippet)):
        try:
            snippets.append(parse_snippet(snippet_node, graph, creation_info.document_namespace))
        except SPDXParsingError as err:
            logger.extend(err.get_messages())

    raise_parsing_error_if_logger_has_messages(logger)
    document = construct_or_raise_parsing_error(Document, dict(creation_info=creation_info, snippets=snippets))
    return document
