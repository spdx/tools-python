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
from rdflib import Graph, URIRef, BNode, RDF, Literal

from spdx.model.checksum import Checksum
from spdx.writer.rdf.writer_utils import spdx_namespace


def add_checksum_information_to_graph(checksum: Checksum, graph: Graph, parent_node: URIRef):
    checksum_node = BNode()
    graph.add((checksum_node, RDF.type, spdx_namespace.Checksum))
    graph.add((checksum_node, spdx_namespace.algorithm,
               spdx_namespace[f"checksumAlgorithm_{checksum.algorithm.name.lower()}"]))
    graph.add((checksum_node, spdx_namespace.checksumValue, Literal(checksum.value)))

    graph.add((parent_node, spdx_namespace.checksum, checksum_node))
