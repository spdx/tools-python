# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import os

import pytest
from rdflib import BNode, Graph, URIRef

from spdx_tools.spdx.model import ChecksumAlgorithm
from spdx_tools.spdx.parser.error import SPDXParsingError
from spdx_tools.spdx.parser.rdf.checksum_parser import convert_rdf_to_algorithm, parse_checksum
from spdx_tools.spdx.rdfschema.namespace import SPDX_NAMESPACE


def test_parse_checksum():
    graph = Graph().parse(os.path.join(os.path.dirname(__file__), "data/file_to_test_rdf_parser.rdf.xml"))
    checksum_node = graph.value(
        subject=URIRef("https://some.namespace#DocumentRef-external"), predicate=SPDX_NAMESPACE.checksum
    )
    assert isinstance(checksum_node, BNode)

    checksum = parse_checksum(checksum_node, graph)

    assert checksum.algorithm == ChecksumAlgorithm.SHA1
    assert checksum.value == "71c4025dd9897b364f3ebbb42c484ff43d00791c"


@pytest.mark.parametrize(
    "rdf_element,expected",
    [
        (SPDX_NAMESPACE.checksumAlgorithm_sha1, ChecksumAlgorithm.SHA1),
        (SPDX_NAMESPACE.checksumAlgorithm_sha224, ChecksumAlgorithm.SHA224),
        (SPDX_NAMESPACE.checksumAlgorithm_sha256, ChecksumAlgorithm.SHA256),
        (SPDX_NAMESPACE.checksumAlgorithm_sha384, ChecksumAlgorithm.SHA384),
        (SPDX_NAMESPACE.checksumAlgorithm_sha512, ChecksumAlgorithm.SHA512),
        (SPDX_NAMESPACE.checksumAlgorithm_sha3_256, ChecksumAlgorithm.SHA3_256),
        (SPDX_NAMESPACE.checksumAlgorithm_sha3_384, ChecksumAlgorithm.SHA3_384),
        (SPDX_NAMESPACE.checksumAlgorithm_sha3_512, ChecksumAlgorithm.SHA3_512),
        (SPDX_NAMESPACE.checksumAlgorithm_blake2b256, ChecksumAlgorithm.BLAKE2B_256),
        (SPDX_NAMESPACE.checksumAlgorithm_blake2b384, ChecksumAlgorithm.BLAKE2B_384),
        (SPDX_NAMESPACE.checksumAlgorithm_blake2b512, ChecksumAlgorithm.BLAKE2B_512),
        (SPDX_NAMESPACE.checksumAlgorithm_blake3, ChecksumAlgorithm.BLAKE3),
        (SPDX_NAMESPACE.checksumAlgorithm_md2, ChecksumAlgorithm.MD2),
        (SPDX_NAMESPACE.checksumAlgorithm_md4, ChecksumAlgorithm.MD4),
        (SPDX_NAMESPACE.checksumAlgorithm_md5, ChecksumAlgorithm.MD5),
        (SPDX_NAMESPACE.checksumAlgorithm_md6, ChecksumAlgorithm.MD6),
        (SPDX_NAMESPACE.checksumAlgorithm_adler32, ChecksumAlgorithm.ADLER32),
    ],
)
def test_convert_rdf_to_algorithm(rdf_element, expected):
    algorithm = convert_rdf_to_algorithm(rdf_element)

    assert algorithm == expected


@pytest.mark.parametrize(
    "invalid_rdf_element",
    [
        SPDX_NAMESPACE.checksumAlgorithm_blake2b_512,
        SPDX_NAMESPACE.checksumAlgorithm_BLAKE2b_512,
        SPDX_NAMESPACE.checksumAlgorithm_sha3512,
        SPDX_NAMESPACE.checksumAlgorithm_sha513,
        SPDX_NAMESPACE.checksumalgorithm_blake2b_512,
    ],
)
def test_convert_invalid_rdf_to_algorithm(invalid_rdf_element):
    with pytest.raises(SPDXParsingError):
        convert_rdf_to_algorithm(invalid_rdf_element)
