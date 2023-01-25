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
import pytest
from rdflib import Graph, URIRef, Literal

from spdx.model.checksum import ChecksumAlgorithm
from spdx.writer.rdf.checksum_writer import add_checksum_information_to_graph, algorithm_to_rdf_string
from spdx.writer.rdf.writer_utils import spdx_namespace
from tests.spdx.fixtures import checksum_fixture


def test_add_checksum_information_to_graph():
    graph = Graph()
    checksum = checksum_fixture()

    add_checksum_information_to_graph(checksum, graph, URIRef("TestURI"))

    assert (None, None, spdx_namespace.Checksum) in graph
    assert (None, spdx_namespace.algorithm, spdx_namespace.checksumAlgorithm_sha1) in graph
    assert (None, spdx_namespace.checksumValue, Literal("71c4025dd9897b364f3ebbb42c484ff43d00791c")) in graph


@pytest.mark.parametrize("algorithm,expected", [(ChecksumAlgorithm.SHA1, spdx_namespace.checksumAlgorithm_sha1),
                                                (ChecksumAlgorithm.SHA224, spdx_namespace.checksumAlgorithm_sha224),
                                                (ChecksumAlgorithm.SHA256, spdx_namespace.checksumAlgorithm_sha256),
                                                (ChecksumAlgorithm.SHA384, spdx_namespace.checksumAlgorithm_sha384),
                                                (ChecksumAlgorithm.SHA512, spdx_namespace.checksumAlgorithm_sha512),
                                                (ChecksumAlgorithm.SHA3_256, spdx_namespace.checksumAlgorithm_sha3_256),
                                                (ChecksumAlgorithm.SHA3_384, spdx_namespace.checksumAlgorithm_sha3_384),
                                                (ChecksumAlgorithm.SHA3_512, spdx_namespace.checksumAlgorithm_sha3_512),
                                                (ChecksumAlgorithm.BLAKE2B_256,
                                                 spdx_namespace.checksumAlgorithm_blake2b256),
                                                (ChecksumAlgorithm.BLAKE2B_384,
                                                 spdx_namespace.checksumAlgorithm_blake2b384),
                                                (ChecksumAlgorithm.BLAKE2B_512,
                                                 spdx_namespace.checksumAlgorithm_blake2b512),
                                                (ChecksumAlgorithm.BLAKE3, spdx_namespace.checksumAlgorithm_blake3),
                                                (ChecksumAlgorithm.MD2, spdx_namespace.checksumAlgorithm_md2),
                                                (ChecksumAlgorithm.MD4, spdx_namespace.checksumAlgorithm_md4),
                                                (ChecksumAlgorithm.MD5, spdx_namespace.checksumAlgorithm_md5),
                                                (ChecksumAlgorithm.MD6, spdx_namespace.checksumAlgorithm_md6),
                                                (ChecksumAlgorithm.ADLER32, spdx_namespace.checksumAlgorithm_adler32)
                                                ])
def test_algorithm_to_rdf_string(algorithm, expected):
    rdf_element = algorithm_to_rdf_string(algorithm)

    assert rdf_element == expected
