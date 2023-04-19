# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from rdflib import RDF, BNode, Graph, Literal, URIRef

from spdx_tools.spdx.model import Checksum, ChecksumAlgorithm
from spdx_tools.spdx.rdfschema.namespace import SPDX_NAMESPACE


def add_checksum_to_graph(checksum: Checksum, graph: Graph, parent: URIRef):
    checksum_node = BNode()
    graph.add((checksum_node, RDF.type, SPDX_NAMESPACE.Checksum))
    graph.add((checksum_node, SPDX_NAMESPACE.algorithm, algorithm_to_rdf_string(checksum.algorithm)))
    graph.add((checksum_node, SPDX_NAMESPACE.checksumValue, Literal(checksum.value)))

    graph.add((parent, SPDX_NAMESPACE.checksum, checksum_node))


def algorithm_to_rdf_string(algorithm: ChecksumAlgorithm) -> URIRef:
    if "BLAKE2B" in algorithm.name:
        algorithm_rdf_string = algorithm.name.replace("_", "").lower()
    else:
        algorithm_rdf_string = algorithm.name.lower()

    return SPDX_NAMESPACE[f"checksumAlgorithm_{algorithm_rdf_string}"]
