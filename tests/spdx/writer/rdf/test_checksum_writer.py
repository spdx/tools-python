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
from rdflib import Graph, URIRef, Literal

from spdx.writer.rdf.checksum_writer import add_checksum_information_to_graph
from spdx.writer.rdf.writer_utils import spdx_namespace
from tests.spdx.fixtures import checksum_fixture


def test_add_checksum_information_to_graph():
    graph = Graph()
    checksum = checksum_fixture()

    add_checksum_information_to_graph(checksum, graph, URIRef("TestURI"))

    assert (None, None, spdx_namespace().Checksum) in graph
    assert (None, spdx_namespace().algorithm, spdx_namespace().checksumAlgorithm_sha1) in graph
    assert (None, spdx_namespace().checksumValue, Literal("71c4025dd9897b364f3ebbb42c484ff43d00791c")) in graph
