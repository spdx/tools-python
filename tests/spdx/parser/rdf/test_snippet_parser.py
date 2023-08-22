# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import os
from unittest import TestCase

import pytest
from rdflib import RDF, BNode, Graph, Literal, URIRef

from spdx_tools.common.spdx_licensing import spdx_licensing
from spdx_tools.spdx.model import SpdxNoAssertion
from spdx_tools.spdx.parser.error import SPDXParsingError
from spdx_tools.spdx.parser.rdf.snippet_parser import parse_ranges, parse_snippet
from spdx_tools.spdx.rdfschema.namespace import POINTER_NAMESPACE, SPDX_NAMESPACE


def test_parse_snippet():
    graph = Graph().parse(os.path.join(os.path.dirname(__file__), "data/file_to_test_rdf_parser.rdf.xml"))
    snippet_node = graph.value(predicate=RDF.type, object=SPDX_NAMESPACE.Snippet)
    doc_namespace = "https://some.namespace"
    assert isinstance(snippet_node, URIRef)

    snippet = parse_snippet(snippet_node, graph, doc_namespace)

    assert snippet.spdx_id == "SPDXRef-Snippet"
    assert snippet.file_spdx_id == "SPDXRef-File"
    assert snippet.byte_range == (1, 2)
    assert snippet.line_range == (3, 4)
    assert snippet.license_concluded == spdx_licensing.parse("MIT AND GPL-2.0")
    TestCase().assertCountEqual(
        snippet.license_info_in_snippet,
        [spdx_licensing.parse("MIT"), spdx_licensing.parse("GPL-2.0"), SpdxNoAssertion()],
    )
    assert snippet.license_comment == "snippetLicenseComment"
    assert snippet.copyright_text == "licenseCopyrightText"
    assert snippet.comment == "snippetComment"
    assert snippet.name == "snippetName"
    assert snippet.attribution_texts == ["snippetAttributionText"]


@pytest.mark.parametrize(
    "predicate_value_class_member",
    [
        (
            [
                (POINTER_NAMESPACE.startPointer, 1, POINTER_NAMESPACE.ByteOffsetPointer, POINTER_NAMESPACE.offset),
                (POINTER_NAMESPACE.endPointer, 2, POINTER_NAMESPACE.ByteOffsetPointer, POINTER_NAMESPACE.offset),
            ]
        ),
        (
            [
                (POINTER_NAMESPACE.startPointer, 100, POINTER_NAMESPACE.LineCharPointer, POINTER_NAMESPACE.lineNumber),
                (POINTER_NAMESPACE.endPointer, 200, POINTER_NAMESPACE.LineCharPointer, POINTER_NAMESPACE.lineNumber),
            ]
        ),
    ],
)
def test_parse_ranges(predicate_value_class_member):
    graph = Graph()
    pointer_class = predicate_value_class_member[0][2]

    add_range_to_graph_helper(graph, predicate_value_class_member)

    range_node = graph.value(predicate=RDF.type, object=POINTER_NAMESPACE.StartEndPointer)
    assert isinstance(range_node, BNode)
    range_dict = parse_ranges(range_node, graph)

    assert pointer_class.fragment in range_dict.keys()
    assert range_dict[pointer_class.fragment][0] == predicate_value_class_member[0][1]
    assert range_dict[pointer_class.fragment][1] == predicate_value_class_member[1][1]


@pytest.mark.parametrize(
    "predicate_value_class_member",
    [
        (
            [
                (POINTER_NAMESPACE.startPointer, 1, POINTER_NAMESPACE.ByteOffsetPointer, POINTER_NAMESPACE.lineNumber),
                (POINTER_NAMESPACE.endPointer, 2, POINTER_NAMESPACE.ByteOffsetPointer, POINTER_NAMESPACE.lineNumber),
            ]
        ),
        (
            [
                (POINTER_NAMESPACE.startPointer, 100, POINTER_NAMESPACE.LineCharPointer, POINTER_NAMESPACE.offset),
                (POINTER_NAMESPACE.endPointer, 200, POINTER_NAMESPACE.LineCharPointer, POINTER_NAMESPACE.offset),
            ]
        ),
    ],
)
def test_parse_ranges_wrong_pair_of_pointer_classes(predicate_value_class_member):
    graph = Graph()
    pointer_class = predicate_value_class_member[0][2]

    add_range_to_graph_helper(graph, predicate_value_class_member)

    range_node = graph.value(predicate=RDF.type, object=POINTER_NAMESPACE.StartEndPointer)
    assert isinstance(range_node, BNode)
    range_dict = parse_ranges(range_node, graph)

    assert pointer_class.fragment in range_dict.keys()
    assert range_dict[pointer_class.fragment][0] is None
    assert range_dict[pointer_class.fragment][1] is None


@pytest.mark.parametrize(
    "predicate_value_class_member,expected_message",
    [
        (
            [
                (POINTER_NAMESPACE.endPointer, 1, POINTER_NAMESPACE.ByteOffsetPointer, POINTER_NAMESPACE.offset),
                (POINTER_NAMESPACE.endPointer, 2, POINTER_NAMESPACE.ByteOffsetPointer, POINTER_NAMESPACE.offset),
            ],
            "Couldn't find pointer of type startPointer.",
        ),
        (
            [(POINTER_NAMESPACE.startPointer, 1, POINTER_NAMESPACE.ByteOffsetPointer, POINTER_NAMESPACE.offset)],
            "Couldn't find pointer of type endPointer.",
        ),
        (
            [
                (POINTER_NAMESPACE.startPointer, 1, POINTER_NAMESPACE.ByteOffsetPointer, POINTER_NAMESPACE.offset),
                (POINTER_NAMESPACE.endPointer, 2, POINTER_NAMESPACE.ByteOffsetPointer, POINTER_NAMESPACE.offset),
                (POINTER_NAMESPACE.endPointer, 3, POINTER_NAMESPACE.ByteOffsetPointer, POINTER_NAMESPACE.offset),
            ],
            "Multiple values for endPointer.",
        ),
        (
            [
                (POINTER_NAMESPACE.startPointer, 100, POINTER_NAMESPACE.LineCharPointer, POINTER_NAMESPACE.lineNumber),
                (POINTER_NAMESPACE.startPointer, 200, POINTER_NAMESPACE.LineCharPointer, POINTER_NAMESPACE.lineNumber),
            ],
            "Multiple values for startPointer",
        ),
        (
            [
                (POINTER_NAMESPACE.startPointer, 100, POINTER_NAMESPACE.LineCharPointer, POINTER_NAMESPACE.lineNumber),
                (POINTER_NAMESPACE.endPointer, 200, POINTER_NAMESPACE.ByteOffsetPointer, POINTER_NAMESPACE.offset),
            ],
            "Types of startPointer and endPointer don't match",
        ),
    ],
)
def test_parse_ranges_error(predicate_value_class_member, expected_message):
    graph = Graph()

    add_range_to_graph_helper(graph, predicate_value_class_member)

    with pytest.raises(SPDXParsingError, match=expected_message):
        range_node = graph.value(predicate=RDF.type, object=POINTER_NAMESPACE.StartEndPointer)
        assert isinstance(range_node, BNode)
        parse_ranges(range_node, graph)


def add_range_to_graph_helper(graph, predicate_value_class_member):
    start_end_pointer = BNode()
    graph.add((start_end_pointer, RDF.type, POINTER_NAMESPACE.StartEndPointer))
    for predicate, value, pointer_class, pointer_member in predicate_value_class_member:
        pointer_node = BNode()
        graph.add((pointer_node, RDF.type, pointer_class))
        graph.add((start_end_pointer, predicate, pointer_node))
        graph.add((pointer_node, pointer_member, Literal(value)))


def test_parse_invalid_file():
    graph = Graph().parse(os.path.join(os.path.dirname(__file__), "data/invalid_documents/file_without_spdx_ids.xml"))
    snippet_node = graph.value(predicate=RDF.type, object=SPDX_NAMESPACE.Snippet)
    doc_namespace = "https://some.namespace"

    assert isinstance(snippet_node, BNode)
    with pytest.raises(SPDXParsingError):
        parse_snippet(snippet_node, graph, doc_namespace)
