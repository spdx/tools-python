# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0

from spdx_tools.spdx.model import ExternalPackageRef, ExternalPackageRefCategory


def test_correct_initialization():
    external_package_reference = ExternalPackageRef(ExternalPackageRefCategory.OTHER, "type", "locator", "comment")
    assert external_package_reference.category == ExternalPackageRefCategory.OTHER
    assert external_package_reference.reference_type == "type"
    assert external_package_reference.locator == "locator"
    assert external_package_reference.comment == "comment"
