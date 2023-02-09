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
from spdx.parser.error import SPDXParsingError

from spdx.model.checksum import Checksum, ChecksumAlgorithm
from spdx.parser.logger import Logger
from spdx.parser.parsing_functions import construct_or_raise_parsing_error, raise_parsing_error_if_logger_has_messages
from spdx.parser.rdf.graph_parsing_functions import parse_literal, remove_prefix
from spdx.rdfschema.namespace import SPDX_NAMESPACE


def parse_checksum(parent_node: URIRef, graph: Graph) -> Checksum:
    logger = Logger()
    algorithm = parse_literal(logger, graph, parent_node, SPDX_NAMESPACE.algorithm,
                              parsing_method=convert_rdf_to_algorithm)
    value = parse_literal(logger, graph, parent_node, SPDX_NAMESPACE.checksumValue)

    raise_parsing_error_if_logger_has_messages(logger, "Checksum")
    checksum = construct_or_raise_parsing_error(Checksum, dict(algorithm=algorithm, value=value))
    return checksum


def convert_rdf_to_algorithm(algorithm: str) -> ChecksumAlgorithm:
    algorithm = remove_prefix(algorithm, SPDX_NAMESPACE.checksumAlgorithm_).upper()
    if "BLAKE2B" in algorithm:
        algorithm = algorithm.replace("BLAKE2B", "BLAKE2B_")
    try:
        checksum = ChecksumAlgorithm[algorithm]
    except KeyError:
        raise SPDXParsingError([f"Invalid value for ChecksumAlgorithm: {algorithm}"])
    return checksum
