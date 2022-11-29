# Copyright (c) 2022 spdx contributors
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

from spdx.checksum import ChecksumAlgorithm, Checksum


@pytest.mark.parametrize("algorithm,expected",
                         [("SHA1", "checksumAlgorithm_sha1"), ("SHA224", "checksumAlgorithm_sha224"),
                          ("SHA3_256", "checksumAlgorithm_sha3_256"), ("BLAKE2B_256", "checksumAlgorithm_blake2b256"),
                          ("MD5", "checksumAlgorithm_md5")])
def test_checksum_to_rdf(algorithm, expected):
    test_algorithm = ChecksumAlgorithm[algorithm]
    rdf_algorithm = test_algorithm.algorithm_to_rdf_representation()

    assert rdf_algorithm == expected


@pytest.mark.parametrize("expected,rdf_algorithm",
                         [(ChecksumAlgorithm.SHA1, "checksumAlgorithm_sha1"),
                          (ChecksumAlgorithm.SHA224, "checksumAlgorithm_sha224"),
                          (ChecksumAlgorithm.SHA3_256, "checksumAlgorithm_sha3_256"),
                          (ChecksumAlgorithm.BLAKE2B_256, "checksumAlgorithm_blake2b256"),
                          (ChecksumAlgorithm.MD5, "checksumAlgorithm_md5")])
def test_checksum_from_rdf(rdf_algorithm, expected):
    algorithm = ChecksumAlgorithm.checksum_from_rdf(rdf_algorithm)

    assert algorithm == expected


@pytest.mark.parametrize("rdf_algorithm",
                         ["_checksumAlgorithm_sha1", "checksumAlgorithm_sha_224", "checksumAlgorithm_sha3256",
                          "checksumAlgorithm_blake2b 256", "checksumAlgorithm_blake2b-256",
                          "checksumAlgorithm_bblake2b 256"])
def test_checksum_from_wrong_rdf(rdf_algorithm):
    with pytest.raises(ValueError) as error:
        ChecksumAlgorithm.checksum_from_rdf(rdf_algorithm)

    assert str(error.value).startswith("Invalid algorithm for checksum")


CHECKSUM_VALUE = "123Abc"


@pytest.mark.parametrize("checksum_string,expected",
                         [("SHA1: " + CHECKSUM_VALUE, Checksum(ChecksumAlgorithm.SHA1, CHECKSUM_VALUE)),
                          ("SHA3-256: " + CHECKSUM_VALUE, Checksum(ChecksumAlgorithm.SHA3_256, CHECKSUM_VALUE)),
                          ("ADLER32: " + CHECKSUM_VALUE, Checksum(ChecksumAlgorithm.ADLER32, CHECKSUM_VALUE)),
                          ("BLAKE3: " + CHECKSUM_VALUE, Checksum(ChecksumAlgorithm.BLAKE3, CHECKSUM_VALUE)),
                          ("BLAKE2b-256: " + CHECKSUM_VALUE, Checksum(ChecksumAlgorithm.BLAKE2B_256, CHECKSUM_VALUE)),
                          ("MD5: " + CHECKSUM_VALUE, Checksum(ChecksumAlgorithm.MD5, CHECKSUM_VALUE))])
def test_checksum_from_string(checksum_string: str, expected: Checksum):
    checksum: Checksum = Checksum.checksum_from_string(checksum_string)
    assert checksum == expected


@pytest.mark.parametrize("checksum, expected",
                         [(Checksum(ChecksumAlgorithm.SHA1, CHECKSUM_VALUE), "SHA1: " + CHECKSUM_VALUE),
                          (Checksum(ChecksumAlgorithm.SHA3_256, CHECKSUM_VALUE), "SHA3-256: " + CHECKSUM_VALUE),
                          (Checksum(ChecksumAlgorithm.ADLER32, CHECKSUM_VALUE), "ADLER32: " + CHECKSUM_VALUE),
                          (Checksum(ChecksumAlgorithm.BLAKE3, CHECKSUM_VALUE), "BLAKE3: " + CHECKSUM_VALUE),
                          (Checksum(ChecksumAlgorithm.BLAKE2B_256, CHECKSUM_VALUE), "BLAKE2b-256: " + CHECKSUM_VALUE),
                          (Checksum(ChecksumAlgorithm.MD5, CHECKSUM_VALUE), "MD5: " + CHECKSUM_VALUE)])
def test_checksum_to_tv(checksum: Checksum, expected: str):
    checksum_string: str = checksum.to_tv()
    assert checksum_string == expected
