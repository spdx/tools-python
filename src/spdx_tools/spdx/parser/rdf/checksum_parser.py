# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from rdflib import BNode, Graph

from spdx_tools.spdx.model import Checksum, ChecksumAlgorithm
from spdx_tools.spdx.parser.error import SPDXParsingError
from spdx_tools.spdx.parser.logger import Logger
from spdx_tools.spdx.parser.parsing_functions import (
    construct_or_raise_parsing_error,
    raise_parsing_error_if_logger_has_messages,
)
from spdx_tools.spdx.parser.rdf.graph_parsing_functions import parse_literal, remove_prefix
from spdx_tools.spdx.rdfschema.namespace import SPDX_NAMESPACE


def parse_checksum(parent_node: BNode, graph: Graph) -> Checksum:
    logger = Logger()
    algorithm = parse_literal(
        logger, graph, parent_node, SPDX_NAMESPACE.algorithm, parsing_method=convert_rdf_to_algorithm
    )
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
