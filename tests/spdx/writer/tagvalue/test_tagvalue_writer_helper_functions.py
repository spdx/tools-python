# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from spdx.model.relationship import RelationshipType
from spdx.writer.tagvalue.tagvalue_writer_helper_functions import scan_relationships
from tests.spdx.fixtures import file_fixture, package_fixture, relationship_fixture


def test_scan_relationships():
    first_package_spdx_id = "SPDXRef-Package1"
    second_package_spdx_id = "SPDXRef-Package2"
    packages = [package_fixture(spdx_id=first_package_spdx_id), package_fixture(spdx_id=second_package_spdx_id)]
    file_spdx_id = "SPDXRef-File"
    files = [file_fixture(spdx_id=file_spdx_id)]
    relationships = [
        relationship_fixture(
            spdx_element_id=first_package_spdx_id,
            relationship_type=RelationshipType.CONTAINS,
            related_spdx_element_id=file_spdx_id,
            comment=None,
        ),
        relationship_fixture(
            spdx_element_id=second_package_spdx_id,
            relationship_type=RelationshipType.CONTAINS,
            related_spdx_element_id=file_spdx_id,
            comment=None,
        ),
    ]

    relationships_to_write, contained_files_by_package_id = scan_relationships(relationships, packages, files)

    assert relationships_to_write == []
    assert contained_files_by_package_id == {first_package_spdx_id: files, second_package_spdx_id: files}
