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
from spdx.writer.rdf.writer_utils import SPDX_NAMESPACE
from tests.spdx.fixtures import file_fixture


def test_add_file_information_to_graph():
    graph = Graph()
    file = file_fixture()

    add_file_information_to_graph(file, graph, "docNamespace", {})

    assert (URIRef("docNamespace#SPDXRef-File"), RDF.type, SPDX_NAMESPACE.File) in graph
    assert (None, SPDX_NAMESPACE.fileName, Literal("./fileName.py")) in graph
    assert (None, SPDX_NAMESPACE.fileType, SPDX_NAMESPACE.fileType_text) in graph
    assert (None, SPDX_NAMESPACE.licenseComments, Literal("licenseComment")) in graph
    assert (None, SPDX_NAMESPACE.licenseConcluded, None) in graph
    assert (None, SPDX_NAMESPACE.licenseInfoInFile, None) in graph
    assert (None, SPDX_NAMESPACE.copyrightText, Literal("copyrightText")) in graph
    assert (None, RDFS.comment, Literal("fileComment")) in graph
    assert (None, SPDX_NAMESPACE.noticeText, Literal("fileNotice")) in graph
    assert (None, SPDX_NAMESPACE.fileContributor, Literal("fileContributor")) in graph
    assert (None, SPDX_NAMESPACE.checksum, None) in graph
    assert (None, SPDX_NAMESPACE.attributionText, Literal("fileAttributionText")) in graph
