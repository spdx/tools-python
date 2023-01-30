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
from rdflib import Graph, Literal, RDFS, RDF, URIRef

from spdx.writer.rdf.file_writer import add_file_information_to_graph
from spdx.writer.rdf.writer_utils import spdx_namespace
from tests.spdx.fixtures import file_fixture


def test_add_file_information_to_graph():
    graph = Graph()
    file = file_fixture()

    add_file_information_to_graph(file, graph, "anyURI", {})

    assert (URIRef("anyURI#SPDXRef-File"), RDF.type, spdx_namespace.File) in graph
    assert (None, spdx_namespace.fileName, Literal("./fileName.py")) in graph
    assert (None, spdx_namespace.fileType, spdx_namespace.fileType_text) in graph
    assert (None, spdx_namespace.licenseComments, Literal("licenseComment")) in graph
    assert (None, spdx_namespace.licenseConcluded, None) in graph
    assert (None, spdx_namespace.licenseInfoInFile, None) in graph
    assert (None, spdx_namespace.copyrightText, Literal("copyrightText")) in graph
    assert (None, RDFS.comment, Literal("fileComment")) in graph
    assert (None, spdx_namespace.noticeText, Literal("fileNotice")) in graph
    assert (None, spdx_namespace.fileContributor, Literal("fileContributor")) in graph
    assert (None, spdx_namespace.checksum, None) in graph
    assert (None, spdx_namespace.attributionText, Literal("fileAttributionText")) in graph
