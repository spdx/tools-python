# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0

import pytest

from spdx_tools.spdx.model import ExternalPackageRef, ExternalPackageRefCategory


def test_correct_initialization():
    external_package_reference = ExternalPackageRef(ExternalPackageRefCategory.OTHER, "type", "locator", "comment")
    assert external_package_reference.category == ExternalPackageRefCategory.OTHER
    assert external_package_reference.reference_type == "type"
    assert external_package_reference.locator == "locator"
    assert external_package_reference.comment == "comment"


def test_wrong_type_in_category():
    with pytest.raises(TypeError):
        ExternalPackageRef([ExternalPackageRefCategory.OTHER], "type", "locator")


def test_wrong_type_in_reference_type():
    with pytest.raises(TypeError):
        ExternalPackageRef(ExternalPackageRefCategory.OTHER, 42, "locator")


def test_wrong_type_in_locator():
    with pytest.raises(TypeError):
        ExternalPackageRef(ExternalPackageRefCategory.OTHER, "type", 42)


def test_wrong_type_in_comment():
    with pytest.raises(TypeError):
        ExternalPackageRef(ExternalPackageRefCategory.OTHER, "type", "locator", [])
