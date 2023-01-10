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
from unittest import TestCase

import pytest

from spdx.model.checksum import ChecksumAlgorithm
from spdx.parser.error import SPDXParsingError
from spdx.parser.jsonlikedict.checksum_parser import ChecksumParser


def test_parse_checksum():
    checksum_parser = ChecksumParser()
    checksum_dict = {
        "algorithm": "SHA1",
        "checksumValue": "d6a770ba38583ed4bb4525bd96e50461655d2759"
    }

    checksum = checksum_parser.parse_checksum(checksum_dict)

    assert checksum.value == "d6a770ba38583ed4bb4525bd96e50461655d2759"
    assert checksum.algorithm == ChecksumAlgorithm.SHA1


def test_parse_invalid_checksum():
    checksum_parser = ChecksumParser()
    checksum_dict = {
        "algorithm": "SHA",
        "checksumValue": "d6a770ba38583ed4bb4525bd96e50461655d2759"
    }

    with pytest.raises(SPDXParsingError) as err:
        checksum_parser.parse_checksum(checksum_dict)

    TestCase().assertCountEqual(err.value.get_messages(),
                                ["Error while parsing Checksum: ['Invalid ChecksumAlgorithm: SHA']"])


def test_parse_incomplete_checksum():
    checksum_parser = ChecksumParser()
    checksum_dict = {
        "algorithm": "SHA1"
    }

    with pytest.raises(SPDXParsingError) as err:
        checksum_parser.parse_checksum(checksum_dict)

    TestCase().assertCountEqual(err.value.get_messages(), [
        "Error while constructing Checksum: ['SetterError Checksum: type of argument \"value\" must be str; got NoneType instead: None']"])
