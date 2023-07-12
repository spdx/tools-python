# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import pytest

from spdx_tools.spdx.model import Checksum, ChecksumAlgorithm, File, PackageVerificationCode
from spdx_tools.spdx.spdx_element_utils import calculate_file_checksum, calculate_package_verification_code


@pytest.fixture
def generate_test_files(tmp_path):
    file_path_1 = tmp_path.joinpath("file1")
    file_path_2 = tmp_path.joinpath("file2")

    with open(file_path_1, "wb") as file:
        file.write(bytes(111))
    with open(file_path_2, "wb") as file:
        file.write(bytes(222))

    yield str(file_path_1), str(file_path_2)


def test_file_checksum_calculation(generate_test_files):
    filepath1, filepath2 = generate_test_files
    checksum = calculate_file_checksum(filepath1, ChecksumAlgorithm.SHA1)
    assert checksum == "dd90903d2f566a3922979dd5e18378a075c7ed33"
    checksum = calculate_file_checksum(filepath2, ChecksumAlgorithm.SHA1)
    assert checksum == "140dc52658e2eeee3fdc4d471cce84fec7253fe3"


def test_verification_code_calculation_with_predefined_checksums(generate_test_files):
    filepath1, filepath2 = generate_test_files
    file1 = File(
        filepath1,
        "SPDXRef-hello",
        [Checksum(ChecksumAlgorithm.SHA1, "20862a6d08391d07d09344029533ec644fac6b21")],
    )
    file2 = File(
        filepath2,
        "SPDXRef-Makefile",
        [Checksum(ChecksumAlgorithm.SHA1, "69a2e85696fff1865c3f0686d6c3824b59915c80")],
    )
    verification_code = calculate_package_verification_code([file1, file2])

    assert verification_code == PackageVerificationCode("c6cb0949d7cd7439fce8690262a0946374824639")


def test_verification_code_calculation_with_calculated_checksums(generate_test_files):
    filepath1, filepath2 = generate_test_files
    file1 = File(
        filepath1,
        "SPDXRef-hello",
        [Checksum(ChecksumAlgorithm.MD4, "20862a6d08391d07d09344029533ec644fac6b21")],
    )
    file2 = File(
        filepath2,
        "SPDXRef-Makefile",
        [Checksum(ChecksumAlgorithm.MD4, "69a2e85696fff1865c3f0686d6c3824b59915c80")],
    )
    verification_code = calculate_package_verification_code([file1, file2])

    assert verification_code == PackageVerificationCode("6f29d813abb63ee52a47dbcb691ea2e70f956328")


def test_verification_code_calculation_with_wrong_file_location():
    unknown_file_name = "./unknown_file_name"
    file1 = File(
        unknown_file_name,
        "SPDXRef-unknown",
        [Checksum(ChecksumAlgorithm.MD4, "20862a6d08391d07d09344029533ec644fac6b21")],
    )

    with pytest.raises(FileNotFoundError) as err:
        calculate_package_verification_code([file1])

    assert unknown_file_name in str(err.value)
