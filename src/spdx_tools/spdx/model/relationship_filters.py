# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from beartype.typing import List

from spdx_tools.spdx.model import Document, Package, Relationship, RelationshipType


def find_package_contains_file_relationships(document: Document, package: Package) -> List[Relationship]:
    file_ids_in_document = [file.spdx_id for file in document.files]
    package_contains_relationships = filter_by_type_and_origin(
        document.relationships, RelationshipType.CONTAINS, package.spdx_id
    )
    return [
        relationship
        for relationship in package_contains_relationships
        if relationship.related_spdx_element_id in file_ids_in_document
    ]


def find_file_contained_by_package_relationships(document: Document, package: Package) -> List[Relationship]:
    file_ids_in_document = [file.spdx_id for file in document.files]
    contained_by_package_relationships = filter_by_type_and_target(
        document.relationships, RelationshipType.CONTAINED_BY, package.spdx_id
    )
    return [
        relationship
        for relationship in contained_by_package_relationships
        if relationship.spdx_element_id in file_ids_in_document
    ]


def filter_by_type_and_target(
    relationships: List[Relationship], relationship_type: RelationshipType, target_id: str
) -> List[Relationship]:
    return [
        relationship
        for relationship in relationships
        if relationship.relationship_type == relationship_type and relationship.related_spdx_element_id == target_id
    ]


def filter_by_type_and_origin(
    relationships: List[Relationship], relationship_type: RelationshipType, origin_id: str
) -> List[Relationship]:
    return [
        relationship
        for relationship in relationships
        if relationship.relationship_type == relationship_type and relationship.spdx_element_id == origin_id
    ]
