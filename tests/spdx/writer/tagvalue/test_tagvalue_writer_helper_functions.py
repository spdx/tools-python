# Copyright (c) 2023 spdx contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#   http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from spdx.model.relationship import RelationshipType
from spdx.writer.tagvalue.tagvalue_writer_helper_functions import scan_relationships
from tests.spdx.fixtures import package_fixture, file_fixture, relationship_fixture


def test_scan_relationships():
    first_package_spdx_id = "SPDXRef-Package1"
    second_package_spdx_id = "SPDXRef-Package2"
    packages = [package_fixture(spdx_id=first_package_spdx_id), package_fixture(spdx_id=second_package_spdx_id)]
    file_spdx_id = "SPDXRef-File"
    files = [file_fixture(spdx_id=file_spdx_id)]
    relationships = [
        relationship_fixture(spdx_element_id=first_package_spdx_id, relationship_type=RelationshipType.CONTAINS,
                             related_spdx_element_id=file_spdx_id, comment=None),
        relationship_fixture(spdx_element_id=second_package_spdx_id, relationship_type=RelationshipType.CONTAINS,
                             related_spdx_element_id=file_spdx_id, comment=None)
    ]

    relationships_to_write, contained_files_by_package_id = scan_relationships(relationships, packages, files)

    assert relationships_to_write == []
    assert contained_files_by_package_id == {first_package_spdx_id: files,
                                             second_package_spdx_id: files}
