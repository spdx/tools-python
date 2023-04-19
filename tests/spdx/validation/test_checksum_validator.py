# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0

from typing import List

import pytest

from spdx_tools.spdx.model import Checksum, ChecksumAlgorithm
from spdx_tools.spdx.validation.checksum_validator import validate_checksum
from spdx_tools.spdx.validation.validation_message import SpdxElementType, ValidationContext, ValidationMessage
from tests.spdx.fixtures import checksum_fixture


@pytest.mark.parametrize(
    "checksum",
    [
        checksum_fixture(),
        Checksum(ChecksumAlgorithm.SHA1, "71c4025dd9897b364f3ebbb42c484ff43d00791c"),
        Checksum(ChecksumAlgorithm.SHA224, "9c9f4e27d957a123cc32d86afe33ae53b1184192cccb23b0f257f588"),
        Checksum(ChecksumAlgorithm.SHA256, "fbea580d286bbbbb41314430d58ba887716a74d7134119c5307cdc9f0c7a4299"),
        Checksum(
            ChecksumAlgorithm.SHA384,
            "73b4ad9a34e5f76cb2525ea6bb8b1dcf9ba79426b3295bd18bc6d148cba4fcc2ca3cf2630fd481b47caaac9127103933",
        ),
        Checksum(
            ChecksumAlgorithm.SHA512,
            "c2aa8a5d297f5e888ce9a30d3745ccc5a628533449a9f98524de3d23695a268f394a67faf8ef370727c2946f1dbbec34aeb7ac10f"
            "15af43e7cb5547f1a464053",
        ),
        Checksum(ChecksumAlgorithm.SHA3_256, "1e772489c042f49aeaae32b00fc5ef170a25afa741cffaafadde597d4d1727ce"),
        Checksum(
            ChecksumAlgorithm.SHA3_384,
            "dd9e30747551865b483bd76bd967384dce0e5670d1b1c3f701cffac7f49b1c46791253493835136b3aa5f679e364c166",
        ),
        Checksum(
            ChecksumAlgorithm.SHA3_512,
            "906bca5580be8c95ae44f775363fb69968ad568898dfb03e0ff96cd9445a0b75f817b68e5c1e80ad624031f851cfddd3a101e1d11"
            "1310266a5d46e2bc1ffbb36",
        ),
        Checksum(ChecksumAlgorithm.BLAKE2B_256, "a0eb3ddfa5807780a562b9c313b2537f1e8dc621e9a524f8c1ffcf07a79e35c7"),
        Checksum(
            ChecksumAlgorithm.BLAKE2B_384,
            "902511afc8939c0193d87857f45a19eddfd7e0413b0f8701a3baaf1b025f882b45a8fbf623fa0ad79b64850ac7a4d0b2",
        ),
        Checksum(
            ChecksumAlgorithm.BLAKE2B_512,
            "72c23b0160e1af3cb159f0cc96210c5e9aecc5a65d4618566776fa6117bf84929dcef56c7f8b087691c23000c945470842d90b5e8"
            "c4af74dce531ca8ebd8824c",
        ),
        Checksum(
            ChecksumAlgorithm.BLAKE3,
            "a872cac2efd29ed2ad8b5faa79b63f983341bea41183582b8863d952f6ac3e1cdfe0189967a13006857d3b9985174bf67239874d"
            "cec4cbbc9839496179feafeda872cac2efd29ed2ad8b5faa79b63f983341bea41183582b8863d952f6ac3e1cdfe0189967a13006"
            "857d3b9985174bf67239874dcec4cbbc9839496179feafed",
        ),
        Checksum(ChecksumAlgorithm.MD2, "af1eec2a1b18886c3f3cc244349d91d8"),
        Checksum(ChecksumAlgorithm.MD4, "d4c41ce30a517d6ce9d79c8c17bb4b66"),
        Checksum(ChecksumAlgorithm.MD5, "0d7f61beb7018b3924c6b8f96549fa39"),
        Checksum(
            ChecksumAlgorithm.MD6,
            "af1eec2a1b18886c3f3cc244349d91d8d4c41ce30a517d6ce9d79c8c17bb4b660d7f61beb7018b3924c6b8f96549fa39",
        ),
        Checksum(ChecksumAlgorithm.ADLER32, "02ec0130"),
    ],
)
def test_valid_checksum(checksum):
    validation_messages: List[ValidationMessage] = validate_checksum(checksum, "parent_id", "SPDX-2.3")

    assert validation_messages == []


@pytest.mark.parametrize(
    "checksum, expected_message",
    [
        (
            Checksum(ChecksumAlgorithm.SHA1, "af1eec2a1b18886c3f3cc244349d91d8"),
            "value of ChecksumAlgorithm.SHA1 must consist of 40 lowercase hexadecimal digits, but is: "
            "af1eec2a1b18886c3f3cc244349d91d8 (length: 32 digits)",
        ),
        (
            Checksum(ChecksumAlgorithm.SHA224, "af1eec2a1b18886c3f3cc244349d91d8"),
            "value of ChecksumAlgorithm.SHA224 must consist of 56 lowercase hexadecimal digits, but is: "
            "af1eec2a1b18886c3f3cc244349d91d8 (length: 32 digits)",
        ),
        (
            Checksum(ChecksumAlgorithm.SHA256, "af1eec2a1b18886c3f3cc244349d91d8"),
            "value of ChecksumAlgorithm.SHA256 must consist of 64 lowercase hexadecimal digits, but is: "
            "af1eec2a1b18886c3f3cc244349d91d8 (length: 32 digits)",
        ),
        (
            Checksum(ChecksumAlgorithm.SHA384, "af1eec2a1b18886c3f3cc244349d91d8"),
            "value of ChecksumAlgorithm.SHA384 must consist of 96 lowercase hexadecimal digits, but is: "
            "af1eec2a1b18886c3f3cc244349d91d8 (length: 32 digits)",
        ),
        (
            Checksum(ChecksumAlgorithm.SHA512, "af1eec2a1b18886c3f3cc244349d91d8"),
            "value of ChecksumAlgorithm.SHA512 must consist of 128 lowercase hexadecimal digits, but is: "
            "af1eec2a1b18886c3f3cc244349d91d8 (length: 32 digits)",
        ),
        (
            Checksum(ChecksumAlgorithm.SHA3_256, "af1eec2a1b18886c3f3cc244349d91d8"),
            "value of ChecksumAlgorithm.SHA3_256 must consist of 64 lowercase hexadecimal digits, but is: "
            "af1eec2a1b18886c3f3cc244349d91d8 (length: 32 digits)",
        ),
        (
            Checksum(ChecksumAlgorithm.SHA3_384, "af1eec2a1b18886c3f3cc244349d91d8"),
            "value of ChecksumAlgorithm.SHA3_384 must consist of 96 lowercase hexadecimal digits, but is: "
            "af1eec2a1b18886c3f3cc244349d91d8 (length: 32 digits)",
        ),
        (
            Checksum(ChecksumAlgorithm.SHA3_512, "af1eec2a1b18886c3f3cc244349d91d8"),
            "value of ChecksumAlgorithm.SHA3_512 must consist of 128 lowercase hexadecimal digits, but is: "
            "af1eec2a1b18886c3f3cc244349d91d8 (length: 32 digits)",
        ),
        (
            Checksum(ChecksumAlgorithm.BLAKE2B_256, "af1eec2a1b18886c3f3cc244349d91d8"),
            "value of ChecksumAlgorithm.BLAKE2B_256 must consist of 64 lowercase hexadecimal digits, but is: "
            "af1eec2a1b18886c3f3cc244349d91d8 (length: 32 digits)",
        ),
        (
            Checksum(ChecksumAlgorithm.BLAKE2B_384, "af1eec2a1b18886c3f3cc244349d91d8"),
            "value of ChecksumAlgorithm.BLAKE2B_384 must consist of 96 lowercase hexadecimal digits, but is: "
            "af1eec2a1b18886c3f3cc244349d91d8 (length: 32 digits)",
        ),
        (
            Checksum(ChecksumAlgorithm.BLAKE2B_512, "af1eec2a1b18886c3f3cc244349d91d8"),
            "value of ChecksumAlgorithm.BLAKE2B_512 must consist of 128 lowercase hexadecimal digits, but is: "
            "af1eec2a1b18886c3f3cc244349d91d8 (length: 32 digits)",
        ),
        (
            Checksum(ChecksumAlgorithm.BLAKE3, "af1eec2a1b18886c3f3cc244349d91d8"),
            "value of ChecksumAlgorithm.BLAKE3 must consist of at least 256 lowercase hexadecimal digits, but is: af1e"
            "ec2a1b18886c3f3cc244349d91d8 (length: 32 digits)",
        ),
        (
            Checksum(ChecksumAlgorithm.MD2, "71c4025dd9897b364f3ebbb42c484ff43d00791c"),
            "value of ChecksumAlgorithm.MD2 must consist of 32 lowercase hexadecimal digits, but is: 71c4025dd9897b364"
            "f3ebbb42c484ff43d00791c (length: 40 digits)",
        ),
        (
            Checksum(ChecksumAlgorithm.MD4, "71c4025dd9897b364f3ebbb42c484ff43d00791c"),
            "value of ChecksumAlgorithm.MD4 must consist of 32 lowercase hexadecimal digits, but is: 71c4025dd9897b364"
            "f3ebbb42c484ff43d00791c (length: 40 digits)",
        ),
        (
            Checksum(ChecksumAlgorithm.MD5, "71c4025dd9897b364f3ebbb42c484ff43d00791c"),
            "value of ChecksumAlgorithm.MD5 must consist of 32 lowercase hexadecimal digits, but is: 71c4025dd9897b364"
            "f3ebbb42c484ff43d00791c (length: 40 digits)",
        ),
        (
            Checksum(
                ChecksumAlgorithm.MD6,
                "a872cac2efd29ed2ad8b5faa79b63f983341bea41183582b8863d952f6ac3e1cdfe0189967a13006857d3b9985174bf672398"
                "74dcec4cbbc9839496179feafeda872cac2efd29ed2ad8b5faa79b63f983341bea41183582b8863d952f6ac3e1cdfe0189967"
                "a13006857d3b9985174bf67239874dcec4cbbc9839496179feafeda872cac2efd29ed2ad8b5faa79b63f983341bea41183582"
                "b8863d952f6ac3e1cdfe0189967a13006857d3b9985174bf67239874dcec4cbbc9839496179feafeda872cac2efd29ed2ad8b"
                "5faa79b63f983341bea41183582b8863d952f6ac3e1cdfe0189967a13006857d3b9985174bf67239874dcec4cbbc983949617"
                "9feafed5",
            ),
            "value of ChecksumAlgorithm.MD6 must consist of between 0 and 512 lowercase hexadecimal digits, but is: "
            "a872cac2efd29ed2ad8b5faa79b63f983341bea41183582b8863d952f6ac3e1cdfe0189967a13006857d3b9985174bf67239874dc"
            "ec4cbbc9839496179feafeda872cac2efd29ed2ad8b5faa79b63f983341bea41183582b8863d952f6ac3e1cdfe0189967a1300685"
            "7d3b9985174bf67239874dcec4cbbc9839496179feafeda872cac2efd29ed2ad8b5faa79b63f983341bea41183582b8863d952f6a"
            "c3e1cdfe0189967a13006857d3b9985174bf67239874dcec4cbbc9839496179feafeda872cac2efd29ed2ad8b5faa79b63f983341"
            "bea41183582b8863d952f6ac3e1cdfe0189967a13006857d3b9985174bf67239874dcec4cbbc9839496179feafed5 "
            "(length: 513 digits)",
        ),
        (
            Checksum(ChecksumAlgorithm.ADLER32, "af1eec2a1b18886c3f3cc244349d91d8"),
            "value of ChecksumAlgorithm.ADLER32 must consist of 8 lowercase hexadecimal digits, but is: "
            "af1eec2a1b18886c3f3cc244349d91d8 (length: 32 digits)",
        ),
        (
            Checksum(ChecksumAlgorithm.SHA1, "CE9F343C4BA371746FD7EAD9B59031AE34D8AFC4"),
            "value of ChecksumAlgorithm.SHA1 must consist of 40 lowercase hexadecimal digits, but is: "
            "CE9F343C4BA371746FD7EAD9B59031AE34D8AFC4 (length: 40 digits)",
        ),
    ],
)
def test_invalid_checksum(checksum, expected_message):
    parent_id = "parent_id"
    validation_messages: List[ValidationMessage] = validate_checksum(checksum, parent_id, "SPDX-2.3")

    expected = ValidationMessage(
        expected_message,
        ValidationContext(parent_id=parent_id, element_type=SpdxElementType.CHECKSUM, full_element=checksum),
    )

    assert validation_messages == [expected]


@pytest.mark.parametrize(
    "checksum",
    [
        Checksum(ChecksumAlgorithm.SHA3_256, "1e772489c042f49aeaae32b00fc5ef170a25afa741cffaafadde597d4d1727ce"),
        Checksum(
            ChecksumAlgorithm.SHA3_384,
            "dd9e30747551865b483bd76bd967384dce0e5670d1b1c3f701cffac7f49b1c46791253493835136b3aa5f679e364c166",
        ),
        Checksum(
            ChecksumAlgorithm.SHA3_512,
            "906bca5580be8c95ae44f775363fb69968ad568898dfb03e0ff96cd9445a0b75f817b68e5c1e80ad624031f851cfddd3a101e1d1"
            "11310266a5d46e2bc1ffbb36",
        ),
        Checksum(ChecksumAlgorithm.BLAKE2B_256, "a0eb3ddfa5807780a562b9c313b2537f1e8dc621e9a524f8c1ffcf07a79e35c7"),
        Checksum(
            ChecksumAlgorithm.BLAKE2B_384,
            "902511afc8939c0193d87857f45a19eddfd7e0413b0f8701a3baaf1b025f882b45a8fbf623fa0ad79b64850ac7a4d0b2",
        ),
        Checksum(
            ChecksumAlgorithm.BLAKE2B_512,
            "72c23b0160e1af3cb159f0cc96210c5e9aecc5a65d4618566776fa6117bf84929dcef56c7f8b087691c23000c945470842d90b5e"
            "8c4af74dce531ca8ebd8824c",
        ),
        Checksum(
            ChecksumAlgorithm.BLAKE3,
            "a872cac2efd29ed2ad8b5faa79b63f983341bea41183582b8863d952f6ac3e1cdfe0189967a13006857d3b9985174bf67239874"
            "dcec4cbbc9839496179feafeda872cac2efd29ed2ad8b5faa79b63f983341bea41183582b8863d952f6ac3e1cdfe0189967a13006"
            "857d3b9985174bf67239874dcec4cbbc9839496179feafed",
        ),
        Checksum(ChecksumAlgorithm.ADLER32, "02ec0130"),
    ],
)
def test_v2_3only_checksums(checksum):
    parent_id = "parent_id"
    validation_messages: List[ValidationMessage] = validate_checksum(checksum, parent_id, "SPDX-2.2")

    context = ValidationContext(parent_id=parent_id, element_type=SpdxElementType.CHECKSUM, full_element=checksum)
    expected = ValidationMessage(f"{checksum.algorithm.name} is not supported in SPDX-2.2", context)

    assert validation_messages == [expected]
