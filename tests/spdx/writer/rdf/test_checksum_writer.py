# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import pytest
from rdflib import RDF, Graph, Literal, URIRef

from spdx_tools.spdx.model import ChecksumAlgorithm
from spdx_tools.spdx.rdfschema.namespace import SPDX_NAMESPACE
from spdx_tools.spdx.writer.rdf.checksum_writer import add_checksum_to_graph, algorithm_to_rdf_string
from tests.spdx.fixtures import checksum_fixture


def test_add_checksum_to_graph():
    graph = Graph()
    checksum = checksum_fixture()

    add_checksum_to_graph(checksum, graph, URIRef("parentNode"))

    assert (URIRef("parentNode"), SPDX_NAMESPACE.checksum, None) in graph
    assert (None, RDF.type, SPDX_NAMESPACE.Checksum) in graph
    assert (None, SPDX_NAMESPACE.algorithm, SPDX_NAMESPACE.checksumAlgorithm_sha1) in graph
    assert (None, SPDX_NAMESPACE.checksumValue, Literal(checksum.value)) in graph


@pytest.mark.parametrize(
    "algorithm,expected",
    [
        (ChecksumAlgorithm.SHA1, SPDX_NAMESPACE.checksumAlgorithm_sha1),
        (ChecksumAlgorithm.SHA224, SPDX_NAMESPACE.checksumAlgorithm_sha224),
        (ChecksumAlgorithm.SHA256, SPDX_NAMESPACE.checksumAlgorithm_sha256),
        (ChecksumAlgorithm.SHA384, SPDX_NAMESPACE.checksumAlgorithm_sha384),
        (ChecksumAlgorithm.SHA512, SPDX_NAMESPACE.checksumAlgorithm_sha512),
        (ChecksumAlgorithm.SHA3_256, SPDX_NAMESPACE.checksumAlgorithm_sha3_256),
        (ChecksumAlgorithm.SHA3_384, SPDX_NAMESPACE.checksumAlgorithm_sha3_384),
        (ChecksumAlgorithm.SHA3_512, SPDX_NAMESPACE.checksumAlgorithm_sha3_512),
        (ChecksumAlgorithm.BLAKE2B_256, SPDX_NAMESPACE.checksumAlgorithm_blake2b256),
        (ChecksumAlgorithm.BLAKE2B_384, SPDX_NAMESPACE.checksumAlgorithm_blake2b384),
        (ChecksumAlgorithm.BLAKE2B_512, SPDX_NAMESPACE.checksumAlgorithm_blake2b512),
        (ChecksumAlgorithm.BLAKE3, SPDX_NAMESPACE.checksumAlgorithm_blake3),
        (ChecksumAlgorithm.MD2, SPDX_NAMESPACE.checksumAlgorithm_md2),
        (ChecksumAlgorithm.MD4, SPDX_NAMESPACE.checksumAlgorithm_md4),
        (ChecksumAlgorithm.MD5, SPDX_NAMESPACE.checksumAlgorithm_md5),
        (ChecksumAlgorithm.MD6, SPDX_NAMESPACE.checksumAlgorithm_md6),
        (ChecksumAlgorithm.ADLER32, SPDX_NAMESPACE.checksumAlgorithm_adler32),
    ],
)
def test_algorithm_to_rdf_string(algorithm, expected):
    rdf_element = algorithm_to_rdf_string(algorithm)

    assert rdf_element == expected
