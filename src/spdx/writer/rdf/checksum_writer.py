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

from spdx.model.checksum import Checksum, ChecksumAlgorithm
from spdx.rdfschema.namespace import SPDX_NAMESPACE


def add_checksum_to_graph(checksum: Checksum, graph: Graph, parent: URIRef):
    checksum_node = BNode()
    graph.add((checksum_node, RDF.type, SPDX_NAMESPACE.Checksum))
    graph.add((checksum_node, SPDX_NAMESPACE.algorithm, algorithm_to_rdf_string(checksum.algorithm)))
    graph.add((checksum_node, SPDX_NAMESPACE.checksumValue, Literal(checksum.value)))

    graph.add((parent, SPDX_NAMESPACE.checksum, checksum_node))

def algorithm_to_rdf_string(algorithm: ChecksumAlgorithm) -> URIRef:
    if "BLAKE2B" in algorithm.name:
        algorithm_rdf_string = algorithm.name.replace("_","").lower()
    else:
        algorithm_rdf_string = algorithm.name.lower()

    return SPDX_NAMESPACE[f"checksumAlgorithm_{algorithm_rdf_string}"]
