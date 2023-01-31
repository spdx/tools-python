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
from rdflib import Graph, Literal, RDFS, URIRef
from spdx.writer.rdf.writer_utils import SPDX_NAMESPACE

from spdx.writer.rdf.extracted_licensing_info_writer import add_extracted_licensing_info_to_graph
from tests.spdx.fixtures import extracted_licensing_info_fixture


def test_add_extracted_licensing_info_to_graph():
    graph = Graph()
    extracted_licensing_info = extracted_licensing_info_fixture()

    add_extracted_licensing_info_to_graph(extracted_licensing_info, graph, URIRef("anyURI"), "anyURI")

    assert (URIRef("anyURI"), SPDX_NAMESPACE.hasExtractedLicensingInfo, None) in graph
    assert (None, None, SPDX_NAMESPACE.ExtractedLicensingInfo) in graph
    assert (None, SPDX_NAMESPACE.licenseId, Literal("LicenseRef-1")) in graph
    assert (None, SPDX_NAMESPACE.extractedText, Literal("extractedText")) in graph
    assert (None, RDFS.seeAlso, Literal("https://see.also")) in graph
    assert (None, SPDX_NAMESPACE.name, Literal("licenseName")) in graph
    assert (None, RDFS.comment, Literal("licenseComment")) in graph
