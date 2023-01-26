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
from rdflib import Graph

from spdx.writer.rdf.relationship_writer import add_relationship_info_to_graph
from spdx.writer.rdf.writer_utils import spdx_namespace
from tests.spdx.fixtures import relationship_fixture


def test_add_relationship_info_to_graph():
    relationship = relationship_fixture()
    graph = Graph()
    add_relationship_info_to_graph(relationship, graph, "anyURI", {})

    assert (None, spdx_namespace.relationshipType, spdx_namespace.relationshipType_describes) in graph
    assert (None, spdx_namespace.relatedSpdxElement, None) in graph