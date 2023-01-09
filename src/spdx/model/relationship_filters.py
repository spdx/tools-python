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
from typing import List

from spdx.model.document import Document
from spdx.model.package import Package
from spdx.model.relationship import Relationship, RelationshipType


def find_package_contains_file_relationships(document: Document, package: Package) -> List[Relationship]:
    file_ids_in_document = [file.spdx_id for file in document.files]
    package_contains_relationships = filter_by_type_and_origin(document.relationships, RelationshipType.CONTAINS,
                                                               package.spdx_id)
    return [relationship for relationship in package_contains_relationships if
            relationship.related_spdx_element_id in file_ids_in_document]


def find_file_contained_by_package_relationships(document: Document, package: Package) -> List[Relationship]:
    file_ids_in_document = [file.spdx_id for file in document.files]
    contained_by_package_relationships = filter_by_type_and_target(document.relationships,
                                                                   RelationshipType.CONTAINED_BY, package.spdx_id)
    return [relationship for relationship in contained_by_package_relationships if
            relationship.spdx_element_id in file_ids_in_document]


def filter_by_type_and_target(relationships: List[Relationship], relationship_type: RelationshipType,
                              target_id: str) -> List[Relationship]:
    return [relationship for relationship in relationships if
            relationship.relationship_type == relationship_type and relationship.related_spdx_element_id == target_id]


def filter_by_type_and_origin(relationships: List[Relationship], relationship_type: RelationshipType,
                              origin_id: str) -> List[Relationship]:
    return [relationship for relationship in relationships if
            relationship.relationship_type == relationship_type and relationship.spdx_element_id == origin_id]
