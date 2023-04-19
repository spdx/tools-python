# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import pytest

from spdx_tools.spdx.model import ChecksumAlgorithm
from spdx_tools.spdx.parser.tagvalue.helper_methods import parse_checksum


@pytest.mark.parametrize(
    "checksum_str, algorithm, value",
    [
        (
            "SHA1: d6a770ba38583ed4bb4525bd96e50461655d2759",
            ChecksumAlgorithm.SHA1,
            "d6a770ba38583ed4bb4525bd96e50461655d2759",
        ),
        (
            "SHA224: 9c9f4e27d957a123cc32d86afe33ae53b1184192cccb23b0f257f588",
            ChecksumAlgorithm.SHA224,
            "9c9f4e27d957a123cc32d86afe33ae53b1184192cccb23b0f257f588",
        ),
        (
            "SHA256: fbea580d286bbbbb41314430d58ba887716a74d7134119c5307cdc9f0c7a4299",
            ChecksumAlgorithm.SHA256,
            "fbea580d286bbbbb41314430d58ba887716a74d7134119c5307cdc9f0c7a4299",
        ),
        (
            "SHA384: 73b4ad9a34e5f76cb2525ea6bb8b1dcf9ba79426b3295bd18bc6d148cba4fcc2ca3cf2630fd481b47caaac9127103933",
            ChecksumAlgorithm.SHA384,
            "73b4ad9a34e5f76cb2525ea6bb8b1dcf9ba79426b3295bd18bc6d148cba4fcc2ca3cf2630fd481b47caaac9127103933",
        ),
        (
            "SHA512: c2aa8a5d297f5e888ce9a30d3745ccc5a628533449a9f98524de3d23695a268f394a67faf8ef370727c2946f1dbbec34a"
            "eb7ac10f15af43e7cb5547f1a464053",
            ChecksumAlgorithm.SHA512,
            "c2aa8a5d297f5e888ce9a30d3745ccc5a628533449a9f98524de3d23695a268f394a67faf8ef370727c2946f1dbbec34aeb7ac10f"
            "15af43e7cb5547f1a464053",
        ),
        (
            "SHA3-256: 1e772489c042f49aeaae32b00fc5ef170a25afa741cffaafadde597d4d1727ce",
            ChecksumAlgorithm.SHA3_256,
            "1e772489c042f49aeaae32b00fc5ef170a25afa741cffaafadde597d4d1727ce",
        ),
        (
            "SHA3-384: dd9e30747551865b483bd76bd967384dce0e5670d1b1c3f701cffac7f49b1c46791253493835136b3aa5f679e364c16"
            "6",
            ChecksumAlgorithm.SHA3_384,
            "dd9e30747551865b483bd76bd967384dce0e5670d1b1c3f701cffac7f49b1c46791253493835136b3aa5f679e364c166",
        ),
        (
            "SHA3-512: 906bca5580be8c95ae44f775363fb69968ad568898dfb03e0ff96cd9445a0b75f817b68e5c1e80ad624031f851cfddd"
            "3a101e1d111310266a5d46e2bc1ffbb36",
            ChecksumAlgorithm.SHA3_512,
            "906bca5580be8c95ae44f775363fb69968ad568898dfb03e0ff96cd9445a0b75f817b68e5c1e80ad624031f851cfddd3a101e1d11"
            "1310266a5d46e2bc1ffbb36",
        ),
        (
            "BLAKE2b-256: a0eb3ddfa5807780a562b9c313b2537f1e8dc621e9a524f8c1ffcf07a79e35c7",
            ChecksumAlgorithm.BLAKE2B_256,
            "a0eb3ddfa5807780a562b9c313b2537f1e8dc621e9a524f8c1ffcf07a79e35c7",
        ),
        (
            "BLAKE2B-384: 902511afc8939c0193d87857f45a19eddfd7e0413b0f8701a3baaf1b025f882b45a8fbf623fa0ad79b64850ac7a4"
            "d0b2",
            ChecksumAlgorithm.BLAKE2B_384,
            "902511afc8939c0193d87857f45a19eddfd7e0413b0f8701a3baaf1b025f882b45a8fbf623fa0ad79b64850ac7a4d0b2",
        ),
        (
            "BLAKE2B-512: 72c23b0160e1af3cb159f0cc96210c5e9aecc5a65d4618566776fa6117bf84929dcef56c7f8b087691c23000c945"
            "470842d90b5e8c4af74dce531ca8ebd8824c",
            ChecksumAlgorithm.BLAKE2B_512,
            "72c23b0160e1af3cb159f0cc96210c5e9aecc5a65d4618566776fa6117bf84929dcef56c7f8b087691c23000c945470842d90b5e8"
            "c4af74dce531ca8ebd8824c",
        ),
        (
            "BLAKE3: a872cac2efd29ed2ad8b5faa79b63f983341bea41183582b8863d952f6ac3e1cdfe0189967a13006857d3b9985174bf67"
            "239874dcec4cbbc9839496179feafeda872cac2efd29ed2ad8b5faa79b63f983341bea41183582b8863d952f6ac3e1cdfe0189967"
            "a13006857d3b9985174bf67239874dcec4cbbc9839496179feafed",
            ChecksumAlgorithm.BLAKE3,
            "a872cac2efd29ed2ad8b5faa79b63f983341bea41183582b8863d952f6ac3e1cdfe0189967a13006857d3b9985174bf67239874dc"
            "ec4cbbc9839496179feafeda872cac2efd29ed2ad8b5faa79b63f983341bea41183582b8863d952f6ac3e1cdfe0189967a1300685"
            "7d3b9985174bf67239874dcec4cbbc9839496179feafed",
        ),
        ("MD2: af1eec2a1b18886c3f3cc244349d91d8", ChecksumAlgorithm.MD2, "af1eec2a1b18886c3f3cc244349d91d8"),
        ("MD4: d4c41ce30a517d6ce9d79c8c17bb4b66", ChecksumAlgorithm.MD4, "d4c41ce30a517d6ce9d79c8c17bb4b66"),
        ("MD5: 0d7f61beb7018b3924c6b8f96549fa39", ChecksumAlgorithm.MD5, "0d7f61beb7018b3924c6b8f96549fa39"),
        (
            "MD6: af1eec2a1b18886c3f3cc244349d91d8d4c41ce30a517d6ce9d79c8c17bb4b660d7f61beb7018b3924c6b8f96549fa39",
            ChecksumAlgorithm.MD6,
            "af1eec2a1b18886c3f3cc244349d91d8d4c41ce30a517d6ce9d79c8c17bb4b660d7f61beb7018b3924c6b8f96549fa39",
        ),
        ("ADLER32: 02ec0130", ChecksumAlgorithm.ADLER32, "02ec0130"),
    ],
)
def test_parse_checksum(checksum_str, algorithm, value):
    checksum = parse_checksum(checksum_str)

    assert checksum.algorithm == algorithm
    assert checksum.value == value
