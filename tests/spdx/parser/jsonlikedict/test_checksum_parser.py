# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from unittest import TestCase

import pytest

from spdx_tools.spdx.model import ChecksumAlgorithm
from spdx_tools.spdx.parser.error import SPDXParsingError
from spdx_tools.spdx.parser.jsonlikedict.checksum_parser import ChecksumParser


def test_parse_checksum():
    checksum_parser = ChecksumParser()
    checksum_dict = {"algorithm": "SHA1", "checksumValue": "d6a770ba38583ed4bb4525bd96e50461655d2759"}

    checksum = checksum_parser.parse_checksum(checksum_dict)

    assert checksum.value == "d6a770ba38583ed4bb4525bd96e50461655d2759"
    assert checksum.algorithm == ChecksumAlgorithm.SHA1


def test_parse_invalid_checksum():
    checksum_parser = ChecksumParser()
    checksum_dict = {"algorithm": "SHA", "checksumValue": "d6a770ba38583ed4bb4525bd96e50461655d2759"}

    with pytest.raises(SPDXParsingError) as err:
        checksum_parser.parse_checksum(checksum_dict)

    TestCase().assertCountEqual(
        err.value.get_messages(), ["Error while parsing Checksum: ['Invalid ChecksumAlgorithm: SHA']"]
    )


def test_parse_incomplete_checksum():
    checksum_parser = ChecksumParser()
    checksum_dict = {"algorithm": "SHA1"}

    with pytest.raises(SPDXParsingError):
        checksum_parser.parse_checksum(checksum_dict)
