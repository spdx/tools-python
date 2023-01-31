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

from rdflib import Graph, URIRef, RDF, RDFS, Literal, BNode

from spdx.writer.rdf.license_expression_writer import add_license_expression_or_none_or_no_assertion
from spdx.writer.rdf.writer_utils import SPDX_NAMESPACE, add_literal_value, add_namespace_to_spdx_id, POINTER_NAMESPACE

from spdx.model.snippet import Snippet


def add_snippet_information_to_graph(snippet: Snippet, graph: Graph, doc_namespace: str,
                                     external_doc_ref_to_namespace: Dict[str, str]):
    snippet_resource = URIRef(add_namespace_to_spdx_id(snippet.spdx_id, doc_namespace, external_doc_ref_to_namespace))
    graph.add((snippet_resource, RDF.type, SPDX_NAMESPACE.Snippet))

    snippet_from_file_ref = URIRef(
        add_namespace_to_spdx_id(snippet.file_spdx_id, doc_namespace, external_doc_ref_to_namespace))
    graph.add((snippet_resource, SPDX_NAMESPACE.snippetFromFile,
               snippet_from_file_ref))
    add_range_to_graph(graph, snippet_resource, snippet.byte_range, snippet_from_file_ref,
                       POINTER_NAMESPACE.ByteOffsetPointer)
    add_range_to_graph(graph, snippet_resource, snippet.line_range, snippet_from_file_ref,
                       POINTER_NAMESPACE.LineCharPointer)
    add_license_expression_or_none_or_no_assertion(graph, snippet_resource, SPDX_NAMESPACE.licenseConcluded,
                                                   snippet.license_concluded, doc_namespace)
    add_license_expression_or_none_or_no_assertion(graph, snippet_resource, SPDX_NAMESPACE.licenseInfoInSnippet,
                                                   snippet.license_info_in_snippet, doc_namespace)
    add_literal_value(graph, snippet_resource, SPDX_NAMESPACE.licenseComments, snippet.license_comment)
    add_literal_value(graph, snippet_resource, SPDX_NAMESPACE.copyrightText, snippet.copyright_text)
    add_literal_value(graph, snippet_resource, RDFS.comment, snippet.comment)
    add_literal_value(graph, snippet_resource, SPDX_NAMESPACE.name, snippet.name)
    for attribution_text in snippet.attribution_texts:
        graph.add((snippet_resource, SPDX_NAMESPACE.attributionText, Literal(attribution_text)))


def add_range_to_graph(graph: Graph, snippet_resource: URIRef, range_information: Optional[Tuple[int, int]],
                       snippet_from_file_ref: URIRef, pointer_class: URIRef):
    start_end_pointer = BNode()
    graph.add((start_end_pointer, RDF.type, POINTER_NAMESPACE.StartEndPointer))
    for (predicate, value) in [(POINTER_NAMESPACE.startPointer, range_information[0]),
                               (POINTER_NAMESPACE.endPointer, range_information[1])]:
        pointer_node = BNode()
        graph.add((pointer_node, RDF.type, pointer_class))
        graph.add((start_end_pointer, predicate, pointer_node))
        graph.add((pointer_node, POINTER_NAMESPACE.reference, snippet_from_file_ref))
        if pointer_class == POINTER_NAMESPACE.ByteOffsetPointer:
            graph.add((pointer_node, POINTER_NAMESPACE.offset, Literal(str(value))))
        else:
            graph.add((pointer_node, POINTER_NAMESPACE.lineNumber, Literal(str(value))))

    graph.add((snippet_resource, SPDX_NAMESPACE.range, start_end_pointer))
