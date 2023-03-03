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
import os
from unittest import TestCase

import pytest
from license_expression import get_spdx_licensing
from rdflib import Graph, RDF, BNode, Literal

from spdx.model.spdx_no_assertion import SpdxNoAssertion
from spdx.parser.error import SPDXParsingError
from spdx.parser.rdf.snippet_parser import parse_snippet, parse_ranges
from spdx.rdfschema.namespace import SPDX_NAMESPACE, POINTER_NAMESPACE


def test_parse_snippet():
    graph = Graph().parse(os.path.join(os.path.dirname(__file__), "data/file_to_test_rdf_parser.rdf.xml"))
    snippet_node = graph.value(predicate=RDF.type, object=SPDX_NAMESPACE.Snippet)
    doc_namespace = "https://some.namespace"

    snippet = parse_snippet(snippet_node, graph, doc_namespace)

    assert snippet.spdx_id == "SPDXRef-Snippet"
    assert snippet.file_spdx_id == "SPDXRef-File"
    assert snippet.byte_range == (1, 2)
    assert snippet.line_range == (3, 4)
    assert snippet.license_concluded == get_spdx_licensing().parse("MIT AND GPL-2.0")
    TestCase().assertCountEqual(snippet.license_info_in_snippet,
                                [get_spdx_licensing().parse("MIT"), get_spdx_licensing().parse("GPL-2.0"),
                                 SpdxNoAssertion()])
    assert snippet.license_comment == "snippetLicenseComment"
    assert snippet.copyright_text == "licenseCopyrightText"
    assert snippet.comment == "snippetComment"
    assert snippet.name == "snippetName"
    assert snippet.attribution_texts == ["snippetAttributionText"]


@pytest.mark.parametrize("predicate_value_class_member",
                         [([(POINTER_NAMESPACE.startPointer, 1, POINTER_NAMESPACE.ByteOffsetPointer,
                             POINTER_NAMESPACE.offset),
                            (POINTER_NAMESPACE.endPointer, 2, POINTER_NAMESPACE.ByteOffsetPointer,
                             POINTER_NAMESPACE.offset)]),
                          ([(POINTER_NAMESPACE.startPointer, 100, POINTER_NAMESPACE.LineCharPointer,
                             POINTER_NAMESPACE.lineNumber),
                            (POINTER_NAMESPACE.endPointer, 200, POINTER_NAMESPACE.LineCharPointer,
                             POINTER_NAMESPACE.lineNumber)])
                          ])
def test_parse_ranges(predicate_value_class_member):
    graph = Graph()
    pointer_class = predicate_value_class_member[0][2]

    add_range_to_graph_helper(graph, predicate_value_class_member)

    range_dict = parse_ranges(graph.value(predicate=RDF.type, object=POINTER_NAMESPACE.StartEndPointer), graph)

    assert pointer_class.fragment in range_dict.keys()
    assert range_dict[pointer_class.fragment][0] == predicate_value_class_member[0][1]
    assert range_dict[pointer_class.fragment][1] == predicate_value_class_member[1][1]


@pytest.mark.parametrize("predicate_value_class_member",
                         [([(POINTER_NAMESPACE.startPointer, 1, POINTER_NAMESPACE.ByteOffsetPointer,
                             POINTER_NAMESPACE.lineNumber),
                            (POINTER_NAMESPACE.endPointer, 2, POINTER_NAMESPACE.ByteOffsetPointer,
                             POINTER_NAMESPACE.lineNumber)]),
                          ([(POINTER_NAMESPACE.startPointer, 100, POINTER_NAMESPACE.LineCharPointer,
                             POINTER_NAMESPACE.offset),
                            (POINTER_NAMESPACE.endPointer, 200, POINTER_NAMESPACE.LineCharPointer,
                             POINTER_NAMESPACE.offset)])
                          ])
def test_parse_ranges_wrong_pair_of_pointer_classes(predicate_value_class_member):
    graph = Graph()
    pointer_class = predicate_value_class_member[0][2]

    add_range_to_graph_helper(graph, predicate_value_class_member)

    range_dict = parse_ranges(graph.value(predicate=RDF.type, object=POINTER_NAMESPACE.StartEndPointer), graph)

    assert pointer_class.fragment in range_dict.keys()
    assert range_dict[pointer_class.fragment][0] is None
    assert range_dict[pointer_class.fragment][1] is None


@pytest.mark.parametrize(
    "predicate_value_class_member,expected_message",
    [([(POINTER_NAMESPACE.endPointer, 1, POINTER_NAMESPACE.ByteOffsetPointer, POINTER_NAMESPACE.offset),
       (POINTER_NAMESPACE.endPointer, 2, POINTER_NAMESPACE.ByteOffsetPointer, POINTER_NAMESPACE.offset)],
      "Couldn't find pointer of type startPointer."),
     ([(POINTER_NAMESPACE.startPointer, 1, POINTER_NAMESPACE.ByteOffsetPointer, POINTER_NAMESPACE.offset)],
      "Couldn't find pointer of type endPointer."),
     ([(POINTER_NAMESPACE.startPointer, 1, POINTER_NAMESPACE.ByteOffsetPointer, POINTER_NAMESPACE.offset),
       (POINTER_NAMESPACE.endPointer, 2, POINTER_NAMESPACE.ByteOffsetPointer, POINTER_NAMESPACE.offset),
       (POINTER_NAMESPACE.endPointer, 3, POINTER_NAMESPACE.ByteOffsetPointer, POINTER_NAMESPACE.offset)],
      "Multiple values for endPointer."),
     ([(POINTER_NAMESPACE.startPointer, 100, POINTER_NAMESPACE.LineCharPointer, POINTER_NAMESPACE.lineNumber),
       (POINTER_NAMESPACE.startPointer, 200, POINTER_NAMESPACE.LineCharPointer, POINTER_NAMESPACE.lineNumber)],
      "Multiple values for startPointer"),
     ([(POINTER_NAMESPACE.startPointer, 100, POINTER_NAMESPACE.LineCharPointer, POINTER_NAMESPACE.lineNumber),
       (POINTER_NAMESPACE.endPointer, 200, POINTER_NAMESPACE.ByteOffsetPointer, POINTER_NAMESPACE.offset)],
      f"Types of startPointer and endPointer don't match")
     ])
def test_parse_ranges_error(predicate_value_class_member, expected_message):
    graph = Graph()

    add_range_to_graph_helper(graph, predicate_value_class_member)

    with pytest.raises(SPDXParsingError, match=expected_message):
        parse_ranges(graph.value(predicate=RDF.type, object=POINTER_NAMESPACE.StartEndPointer), graph)


def add_range_to_graph_helper(graph, predicate_value_class_member):
    start_end_pointer = BNode()
    graph.add((start_end_pointer, RDF.type, POINTER_NAMESPACE.StartEndPointer))
    for (predicate, value, pointer_class, pointer_member) in predicate_value_class_member:
        pointer_node = BNode()
        graph.add((pointer_node, RDF.type, pointer_class))
        graph.add((start_end_pointer, predicate, pointer_node))
        graph.add((pointer_node, pointer_member, Literal(value)))
