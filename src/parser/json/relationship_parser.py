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
from typing import Dict, List, Optional

from src.model.relationship import Relationship, RelationshipType
from src.model.typing.constructor_type_errors import ConstructorTypeErrors
from src.parser.error import SPDXParsingError
from src.parser.json.dict_parsing_functions import append_parsed_field_or_log_error, \
    raise_parsing_error_if_logger_has_messages, json_str_to_enum_name, construct_or_raise_parsing_error, \
    parse_field_or_log_error
from src.parser.logger import Logger


class RelationshipParser:
    logger: Logger

    def __init__(self):
        self.logger = Logger()

    def parse_all_relationships(self, input_doc_dict: Dict) -> List[Relationship]:
        relationships_list = []
        relationships_dicts: List[Dict] = input_doc_dict.get("relationships")
        if relationships_dicts:
            relationships_list.extend(
                parse_field_or_log_error(logger=self.logger, field=relationships_dicts,
                                         parsing_method=self.parse_relationships, default=[]))

        document_describes: List[str] = input_doc_dict.get("documentDescribes")
        doc_spdx_id: str = input_doc_dict.get("SPDXID")
        if document_describes:
            relationships_list.extend(
                parse_field_or_log_error(logger=self.logger, field=document_describes,
                                         parsing_method=lambda x: self.parse_document_describes(doc_spdx_id=doc_spdx_id, described_spdx_ids=x, created_relationships=relationships_list),
                                         default=[]))

            package_dicts: List[Dict] = input_doc_dict.get("packages")
            if package_dicts:
                relationships_list.extend(
                    parse_field_or_log_error(logger=self.logger, field=package_dicts,
                                             parsing_method=lambda x: self.parse_has_files(package_dicts=x, created_relationships=relationships_list),
                                             default=[]))

            file_dicts: List[Dict] = input_doc_dict.get("files")
            if file_dicts:
                # not implemented yet, deal with deprecated fields in file
                relationships_list.extend(
                    parse_field_or_log_error(logger=self.logger, field=file_dicts,
                                             parsing_method=self.parse_file_dependencies, default=[]))

            generated_relationships = self.parse_artifact_of(file_dicts=file_dicts)

            raise_parsing_error_if_logger_has_messages(self.logger)

        return relationships_list

    def parse_relationships(self, relationship_dicts: List[Dict]) -> List[Relationship]:
        logger = Logger()
        relationship_list = []
        for relationship_dict in relationship_dicts:
            relationship_list = append_parsed_field_or_log_error(logger=logger, list_to_append_to=relationship_list,
                                                                 field=relationship_dict, method_to_parse=self.parse_relationship)
        raise_parsing_error_if_logger_has_messages(logger)
        return relationship_list

    def parse_relationship(self, relationship_dict: Dict) -> Relationship:
        logger = Logger()
        spdx_element_id: str = relationship_dict.get("spdxElementId")
        related_spdx_element: str = relationship_dict.get("relatedSpdxElement")
        relationship_type: Optional[RelationshipType] = parse_field_or_log_error(logger=logger,
                                                                                 field=relationship_dict.get("relationshipType"),
                                                                                 parsing_method=self.parse_relationship_type)
        relationship_comment: str = relationship_dict.get("comment")
        raise_parsing_error_if_logger_has_messages(logger, "relationship")

        relationship = construct_or_raise_parsing_error(Relationship, dict(spdx_element_id=spdx_element_id,
                                                                           relationship_type=relationship_type,
                                                                           related_spdx_element_id=related_spdx_element,
                                                                           comment=relationship_comment))
        return relationship

    @staticmethod
    def parse_relationship_type(relationship_type_str: str) -> RelationshipType:
        try:
            relationship_type = RelationshipType[json_str_to_enum_name(relationship_type_str)]
        except KeyError:
            raise SPDXParsingError([f"RelationshipType {relationship_type_str} is not valid."])
        except AttributeError:
            raise SPDXParsingError([f"RelationshipType must be str, not {type(relationship_type_str).__name__}."])
        return relationship_type

    def parse_document_describes(self, doc_spdx_id: str, described_spdx_ids: List[str],
                                 created_relationships: List[Relationship]) -> List[Relationship]:
        logger = Logger()
        describes_relationships = []
        for spdx_id in described_spdx_ids:
            try:
                describes_relationship = Relationship(spdx_element_id=doc_spdx_id,
                                                      relationship_type=RelationshipType.DESCRIBES,
                                                      related_spdx_element_id=spdx_id)
            except ConstructorTypeErrors as err:
                logger.append(err.get_messages())
                continue
            if not self.check_if_relationship_exists(describes_relationship, created_relationships):
                describes_relationships.append(describes_relationship)
        raise_parsing_error_if_logger_has_messages(logger, "describes_relationship")

        return describes_relationships

    def parse_has_files(self, package_dicts: List[Dict], created_relationships: List[Relationship]) -> List[
        Relationship]:
        logger = Logger()
        contains_relationships = []
        for package in package_dicts:
            package_spdx_id = package.get("SPDXID")
            contained_files = package.get("hasFiles")
            if not contained_files:
                continue
            for file_spdx_id in contained_files:
                try:
                    contains_relationship = Relationship(spdx_element_id=package_spdx_id,
                                                         relationship_type=RelationshipType.CONTAINS,
                                                         related_spdx_element_id=file_spdx_id)
                except ConstructorTypeErrors as err:
                    logger.append(err.get_messages())
                    continue
                if not self.check_if_relationship_exists(relationship=contains_relationship,
                                                         created_relationships=created_relationships):
                    contains_relationships.append(contains_relationship)
        raise_parsing_error_if_logger_has_messages(logger, "describes_relationship")

        return contains_relationships

    def check_if_relationship_exists(self, relationship: Relationship,
                                     created_relationships: List[Relationship]) -> bool:
        created_relationships_without_comment: List[Relationship] = self.ignore_any_comments_in_relationship_list(
            created_relationships)
        if relationship in created_relationships_without_comment:
            return True
        relationship_converted: Relationship = self.convert_relationship(relationship)
        if relationship_converted in created_relationships_without_comment:
            return True

        return False

    @staticmethod
    def ignore_any_comments_in_relationship_list(created_relationships: List[Relationship]) -> List[Relationship]:
        relationships_without_comment = [Relationship(relationship_type=relationship.relationship_type,
                                                      related_spdx_element_id=relationship.related_spdx_element_id,
                                                      spdx_element_id=relationship.spdx_element_id) for relationship in
                                         created_relationships]
        return relationships_without_comment

    def convert_relationship(self, relationship: Relationship) -> Relationship:
        return Relationship(related_spdx_element_id=relationship.spdx_element_id,
                            spdx_element_id=relationship.related_spdx_element_id,
                            relationship_type=self.convert_relationship_types[relationship.relationship_type],
                            comment=relationship.comment)

    convert_relationship_types = {RelationshipType.DESCRIBES: RelationshipType.DESCRIBED_BY,
                                  RelationshipType.DESCRIBED_BY: RelationshipType.DESCRIBES,
                                  RelationshipType.CONTAINS: RelationshipType.CONTAINED_BY,
                                  RelationshipType.CONTAINED_BY: RelationshipType.CONTAINS}

    @staticmethod
    def parse_file_dependencies(file_dicts: List[Dict]) -> List[Relationship]:
        logger = Logger()
        dependency_relationships = []
        for file in file_dicts:
            file_spdx_id: str = file.get("SPDXID")
            dependency_of: List[str] = file.get("fileDependencies")
            if not dependency_of:
                continue
            for dependency in dependency_of:
                try:
                    dependency_relationship = Relationship(spdx_element_id=dependency,
                                                           relationship_type=RelationshipType.DEPENDENCY_OF,
                                                           related_spdx_element_id=file_spdx_id)
                except ConstructorTypeErrors as err:
                    logger.extend(err.get_messages())
                    continue
                dependency_relationships.append(dependency_relationship)
        raise_parsing_error_if_logger_has_messages(logger, "dependency relationship")
        return dependency_relationships

    @staticmethod
    def parse_artifact_of(file_dicts: List[Dict]) -> List[Relationship]:
        generated_relationships = []
        # TODO: artifactOfs is deprecated and should be converted to an external package and a generated from relationship
        return generated_relationships
