# Copyright (c) 2014 Ahmed H. Ismail
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
list of checksum algorithms from SPDX spec part 8.4.1 "Description".
SHA1, SHA224, SHA256, SHA384, SHA512, SHA3-256, SHA3-384, SHA3-512,
BLAKE2b-256, BLAKE2b-384, BLAKE2b-512, BLAKE3,
MD2, MD4, MD5, MD6, ADLER32
"""
CHECKSUM_ALGORITHM_TO_XML_DICT = {
    'ADLER32': 'checksumAlgorithm_adler32',
    'BLAKE2b-256': 'checksumAlgorithm_blake2b-256',
    'BLAKE2b-384': 'checksumAlgorithm_blake2b-384',
    'BLAKE2b-512': 'checksumAlgorithm_blake2b-512',
    'BLAKE3': 'checksumAlgorithm_blake3',
    'MD2': 'checksumAlgorithm_md2',
    'MD4': 'checksumAlgorithm_md4',
    'MD5': 'checksumAlgorithm_md5',
    'MD6': 'checksumAlgorithm_md6',
    'SHA1': 'checksumAlgorithm_sha1',
    'SHA224': 'checksumAlgorithm_sha224',
    'SHA256': 'checksumAlgorithm_sha256',
    'SHA384': 'checksumAlgorithm_sha384',
    'SHA512': 'checksumAlgorithm_sha512',
    'SHA3-256': 'checksumAlgorithm_sha3-256',
    'SHA3-384': 'checksumAlgorithm_sha3-384',
    'SHA3-512': 'checksumAlgorithm_sha3-512',
}
CHECKSUM_ALGORITHMS = [k for k in CHECKSUM_ALGORITHM_TO_XML_DICT]
CHECKSUM_ALGORITHM_FROM_XML_DICT = {}
for k, v in CHECKSUM_ALGORITHM_TO_XML_DICT.items():
    CHECKSUM_ALGORITHM_FROM_XML_DICT[v] = k

# regex parses algorithm:value from string
CHECKSUM_REGEX = '({}):\\s*([a-f0-9]*)'.format('|'.join(CHECKSUM_ALGORITHMS))


class Algorithm(object):
    """Generic checksum algorithm."""

    def __init__(self, identifier, value):
        if identifier not in CHECKSUM_ALGORITHMS:
            raise ValueError('checksum algorithm {} is not supported'.format(identifier))
        self.identifier = identifier
        self.value = value

    def to_tv(self):
        return "{0}: {1}".format(self.identifier, self.value)
