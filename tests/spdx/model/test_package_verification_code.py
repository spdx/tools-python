# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0

import pytest

from spdx_tools.spdx.model import PackageVerificationCode


def test_correct_initialization():
    package_verification_code = PackageVerificationCode("value", ["file1", "file2"])
    assert package_verification_code.value == "value"
    assert package_verification_code.excluded_files == ["file1", "file2"]


def test_wrong_type_in_value():
    with pytest.raises(TypeError):
        PackageVerificationCode(42, ["file1", "file2"])


def test_wrong_type_in_excluded_files():
    with pytest.raises(TypeError):
        PackageVerificationCode("value", "file1")
