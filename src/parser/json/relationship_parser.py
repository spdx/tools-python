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
from typing import Dict, List

from src.model.relationship import Relationship, RelationshipType
from src.parser.error import SPDXParsingError
from src.parser.logger import Logger


class RelationshipParser:
    logger: Logger

    def __init__(self):
        self.logger = Logger()

    def parse_relationship(self, relationship_dict: Dict) -> Relationship:
        spdx_element_id = relationship_dict.get("spdxElementId")
        related_spdx_element = relationship_dict.get("relatedSpdxElement")
        relationship_type = relationship_dict.get("relationshipType")
        relationship_comment = relationship_dict.get("comment")
        relationship = Relationship(spdx_element_id=spdx_element_id,
                                    relationship_type=RelationshipType[relationship_type],
                                    related_spdx_element_id=related_spdx_element, comment=relationship_comment)
        return relationship

    def parse_relationships(self, input_doc_dict: Dict) -> List[Relationship]:
        relationships_list = []
        relationships_dicts = input_doc_dict.get("relationships")
        document_describes = input_doc_dict.get("documentDescribes")
        doc_spdx_id = input_doc_dict.get("SPDXID")
        package_dicts = input_doc_dict.get("packages")
        file_dicts = input_doc_dict.get("files")
        if relationships_dicts:
            for relationship_dict in relationships_dicts:
                relationships_list.append(self.parse_relationship(relationship_dict))
        describes_relationships = self.parse_document_describes(doc_spdx_id=doc_spdx_id,
                                                                described_spdx_ids=document_describes,
                                                                created_relationships=relationships_list)
        relationships_list.extend(describes_relationships)
        if package_dicts:
            contains_relationships = self.parse_has_files(package_dicts=package_dicts,
                                                          created_relationships=relationships_list)
            relationships_list.extend(contains_relationships)
        if file_dicts:
            # not implemented yet, deal with deprecated fields in file
            dependency_relationships = self.parse_file_dependencies(file_dicts=file_dicts)
            generated_relationships = self.parse_artifact_of(file_dicts=file_dicts)

        if self.logger.has_messages():
            raise SPDXParsingError(self.logger.get_messages())

        return relationships_list

    def parse_document_describes(self, doc_spdx_id: str, described_spdx_ids: List[str],
                                 created_relationships: List[Relationship]) -> List[Relationship]:
        describes_relationships = []
        for spdx_id in described_spdx_ids:
            describes_relationship = Relationship(spdx_element_id=doc_spdx_id,
                                                  relationship_type=RelationshipType.DESCRIBES,
                                                  related_spdx_element_id=spdx_id)
            if not self.check_if_relationship_exists(describes_relationship, created_relationships):
                describes_relationships.append(describes_relationship)

        return describes_relationships

    def parse_has_files(self, package_dicts: List[Dict], created_relationships: List[Relationship]) -> List[
        Relationship]:
        contains_relationships = []
        for package in package_dicts:
            package_spdx_id = package.get("SPDXID")
            contained_files = package.get("hasFiles")
            if not contained_files:
                continue
            for file_spdx_id in contained_files:
                contains_relationship = Relationship(spdx_element_id=package_spdx_id,
                                                     relationship_type=RelationshipType.CONTAINS,
                                                     related_spdx_element_id=file_spdx_id)
                if not self.check_if_relationship_exists(relationship=contains_relationship,
                                                         created_relationships=created_relationships):
                    contains_relationships.append(contains_relationship)

        return contains_relationships

    def check_if_relationship_exists(self, relationship: Relationship,
                                     created_relationships: List[Relationship]) -> bool:
        created_relationships_without_comment = self.ignore_any_comments_in_relationship_list(created_relationships)
        if relationship in created_relationships_without_comment:
            return True
        relationship_converted = self.convert_relationship(relationship)
        if relationship_converted in created_relationships_without_comment:
            return True

        return False

    def ignore_any_comments_in_relationship_list(self, created_relationships: List[Relationship]) -> List[Relationship]:
        relationships_without_comment = [Relationship(relationship_type=relationship.relationship_type,
                                                      related_spdx_element_id=relationship.related_spdx_element_id,
                                                      spdx_element_id=relationship.spdx_element_id) for relationship in
                                         created_relationships]
        return relationships_without_comment

    def convert_relationship(self, relationship: Relationship) -> Relationship:
        if relationship.relationship_type == RelationshipType.DESCRIBES:
            return Relationship(related_spdx_element_id=relationship.spdx_element_id,
                                spdx_element_id=relationship.related_spdx_element_id,
                                relationship_type=RelationshipType.DESCRIBED_BY, comment=relationship.comment)
        if relationship.relationship_type == RelationshipType.DESCRIBED_BY:
            return Relationship(related_spdx_element_id=relationship.spdx_element_id,
                                spdx_element_id=relationship.related_spdx_element_id,
                                relationship_type=RelationshipType.DESCRIBES, comment=relationship.comment)
        if relationship.relationship_type == RelationshipType.CONTAINS:
            return Relationship(related_spdx_element_id=relationship.spdx_element_id,
                                spdx_element_id=relationship.related_spdx_element_id,
                                relationship_type=RelationshipType.CONTAINED_BY, comment=relationship.comment)
        if relationship.relationship_type == RelationshipType.CONTAINED_BY:
            return Relationship(related_spdx_element_id=relationship.spdx_element_id,
                                spdx_element_id=relationship.related_spdx_element_id,
                                relationship_type=RelationshipType.CONTAINS, comment=relationship.comment)

    def parse_file_dependencies(self, file_dicts: List[Dict]) -> List[Relationship]:
        dependency_relationships = []
        for file in file_dicts:
            file_spdx_id = file.get("SPDXID")
            dependency_of = file.get("fileDependencies")
            if not dependency_of:
                continue
            for dependency in dependency_of:
                dependency_relationships.append(
                    Relationship(spdx_element_id=dependency, relationship_type=RelationshipType.DEPENDENCY_OF,
                                 related_spdx_element_id=file_spdx_id))
        return dependency_relationships

    def parse_artifact_of(self, file_dicts: List[Dict]) -> List[Relationship]:
        generated_relationships = []
        # TODO: artifactOfs is deprecated and should be converted to an external package and a generated from relationship
        return generated_relationships
