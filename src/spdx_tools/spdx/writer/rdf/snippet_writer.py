# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from beartype.typing import Dict, Optional, Tuple
from rdflib import RDF, RDFS, BNode, Graph, Literal, URIRef

from spdx_tools.spdx.model import Snippet
from spdx_tools.spdx.rdfschema.namespace import POINTER_NAMESPACE, SPDX_NAMESPACE
from spdx_tools.spdx.writer.rdf.license_expression_writer import add_license_expression_or_none_or_no_assertion
from spdx_tools.spdx.writer.rdf.writer_utils import add_namespace_to_spdx_id, add_optional_literal


def add_snippet_to_graph(
    snippet: Snippet, graph: Graph, doc_namespace: str, external_doc_ref_to_namespace: Dict[str, str]
):
    snippet_resource = URIRef(add_namespace_to_spdx_id(snippet.spdx_id, doc_namespace, external_doc_ref_to_namespace))
    graph.add((snippet_resource, RDF.type, SPDX_NAMESPACE.Snippet))

    snippet_from_file_ref = URIRef(
        add_namespace_to_spdx_id(snippet.file_spdx_id, doc_namespace, external_doc_ref_to_namespace)
    )
    graph.add((snippet_resource, SPDX_NAMESPACE.snippetFromFile, snippet_from_file_ref))
    add_range_to_graph(
        snippet.byte_range, graph, snippet_resource, snippet_from_file_ref, POINTER_NAMESPACE.ByteOffsetPointer
    )
    add_range_to_graph(
        snippet.line_range, graph, snippet_resource, snippet_from_file_ref, POINTER_NAMESPACE.LineCharPointer
    )
    add_license_expression_or_none_or_no_assertion(
        snippet.license_concluded, graph, snippet_resource, SPDX_NAMESPACE.licenseConcluded, doc_namespace
    )
    add_license_expression_or_none_or_no_assertion(
        snippet.license_info_in_snippet, graph, snippet_resource, SPDX_NAMESPACE.licenseInfoInSnippet, doc_namespace
    )
    add_optional_literal(snippet.license_comment, graph, snippet_resource, SPDX_NAMESPACE.licenseComments)
    add_optional_literal(snippet.copyright_text, graph, snippet_resource, SPDX_NAMESPACE.copyrightText)
    add_optional_literal(snippet.comment, graph, snippet_resource, RDFS.comment)
    add_optional_literal(snippet.name, graph, snippet_resource, SPDX_NAMESPACE.name)
    for attribution_text in snippet.attribution_texts:
        graph.add((snippet_resource, SPDX_NAMESPACE.attributionText, Literal(attribution_text)))


def add_range_to_graph(
    range_information: Optional[Tuple[int, int]],
    graph: Graph,
    snippet_node: URIRef,
    snippet_from_file_ref: URIRef,
    pointer_class: URIRef,
):
    start_end_pointer = BNode()
    graph.add((start_end_pointer, RDF.type, POINTER_NAMESPACE.StartEndPointer))
    for predicate, value in [
        (POINTER_NAMESPACE.startPointer, range_information[0]),
        (POINTER_NAMESPACE.endPointer, range_information[1]),
    ]:
        pointer_node = BNode()
        graph.add((pointer_node, RDF.type, pointer_class))
        graph.add((start_end_pointer, predicate, pointer_node))
        graph.add((pointer_node, POINTER_NAMESPACE.reference, snippet_from_file_ref))
        if pointer_class == POINTER_NAMESPACE.ByteOffsetPointer:
            graph.add((pointer_node, POINTER_NAMESPACE.offset, Literal(value)))
        else:
            graph.add((pointer_node, POINTER_NAMESPACE.lineNumber, Literal(value)))

    graph.add((snippet_node, SPDX_NAMESPACE.range, start_end_pointer))
