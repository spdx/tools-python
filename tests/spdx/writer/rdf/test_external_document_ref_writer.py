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
from rdflib import Graph, URIRef
from spdx.writer.rdf.writer_utils import spdx_namespace

from spdx.writer.rdf.external_document_ref_writer import add_external_document_ref_to_graph
from tests.spdx.fixtures import external_document_ref_fixture


def test_add_external_document_ref_to_graph():
    graph = Graph()
    external_document_ref = external_document_ref_fixture()

    add_external_document_ref_to_graph(external_document_ref, graph, URIRef("anyURI"), "anyURI")

    assert (None, spdx_namespace.externalDocumentRef, URIRef("anyURI#DocumentRef-external")) in graph
    assert (None, None, spdx_namespace.ExternalDocumentRef) in graph
    assert (None, spdx_namespace.checksum, None) in graph
    assert (None, None, spdx_namespace.Checksum) in graph
    assert (None, spdx_namespace.spdxDocument, URIRef("https://namespace.com")) in graph



