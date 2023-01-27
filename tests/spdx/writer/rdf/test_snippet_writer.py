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
from rdflib import Graph, URIRef, RDF, Literal, RDFS
from spdx.writer.rdf.writer_utils import spdx_namespace, pointer_namespace

from spdx.writer.rdf.snippet_writer import add_snippet_information_to_graph, add_range_to_graph
from tests.spdx.fixtures import snippet_fixture


def test_add_snippet_information_to_graph():
    graph = Graph()
    snippet = snippet_fixture()

    add_snippet_information_to_graph(snippet, graph, "anyURI", {})

    assert (URIRef("anyURI#SPDXRef-Snippet"), RDF.type, spdx_namespace.Snippet) in graph
    assert (None, spdx_namespace.snippetFromFile, URIRef(f"anyURI#{snippet.file_spdx_id}")) in graph
    assert (None, spdx_namespace.licenseConcluded, Literal("MIT AND GPL-2.0")) in graph
    assert (None, spdx_namespace.licenseInfoInSnippet, Literal("MIT")) in graph
    assert (None, spdx_namespace.licenseInfoInSnippet, Literal("GPL-2.0")) in graph
    assert (None, spdx_namespace.licenseComments, Literal("snippetLicenseComment")) in graph
    assert (None, spdx_namespace.copyrightText, Literal("licenseCopyrightText")) in graph
    assert (None, spdx_namespace.name, Literal("snippetName")) in graph
    assert (None, spdx_namespace.attributionText, Literal("snippetAttributionText")) in graph
    assert (None, RDFS.comment, Literal("snippetComment")) in graph


def test_add_ranges_to_graph():
    graph = Graph()
    byte_range = (5, 190)

    add_range_to_graph(graph, URIRef("anyUR"), byte_range, URIRef("anyURI#SPDXRef-File"), pointer_namespace.ByteOffsetPointer)

    assert (None, spdx_namespace.range, None) in graph
    assert (None, pointer_namespace.startPointer, None) in graph
    assert (None, pointer_namespace.endPointer, None) in graph
    assert (None, pointer_namespace.reference, URIRef("anyURI#SPDXRef-File")) in graph
    assert (None, pointer_namespace.offset, Literal(str(5))) in graph
    assert (None, pointer_namespace.offset, Literal(str(190))) in graph
