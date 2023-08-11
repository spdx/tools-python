# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from beartype.typing import Dict, List, Optional

from spdx_tools.common.typing.constructor_type_errors import ConstructorTypeErrors
from spdx_tools.spdx.model import Relationship, RelationshipType
from spdx_tools.spdx.parser.error import SPDXParsingError
from spdx_tools.spdx.parser.jsonlikedict.dict_parsing_functions import (
    delete_duplicates_from_list,
    json_str_to_enum_name,
    parse_field_or_log_error,
    parse_field_or_no_assertion_or_none,
)
from spdx_tools.spdx.parser.logger import Logger
from spdx_tools.spdx.parser.parsing_functions import (
    construct_or_raise_parsing_error,
    raise_parsing_error_if_logger_has_messages,
)


class RelationshipParser:
    logger: Logger

    def __init__(self):
        self.logger = Logger()

    def parse_all_relationships(self, input_doc_dict: Dict) -> List[Relationship]:
        relationships = []
        relationship_dicts: List[Dict] = input_doc_dict.get("relationships", [])
        relationships.extend(
            parse_field_or_log_error(self.logger, relationship_dicts, self.parse_relationship, [], True)
        )

        document_describes: List[str] = delete_duplicates_from_list(input_doc_dict.get("documentDescribes", []))
        doc_spdx_id: Optional[str] = input_doc_dict.get("SPDXID")

        existing_relationships_without_comments: List[Relationship] = self.get_all_relationships_without_comments(
            relationships
        )
        relationships.extend(
            parse_field_or_log_error(
                self.logger,
                document_describes,
                lambda x: self.parse_document_describes(
                    doc_spdx_id=doc_spdx_id,
                    described_spdx_ids=x,
                    existing_relationships=existing_relationships_without_comments,
                ),
                [],
            )
        )

        package_dicts: List[Dict] = input_doc_dict.get("packages", [])
        existing_relationships_without_comments: List[Relationship] = self.get_all_relationships_without_comments(
            relationships
        )

        relationships.extend(
            parse_field_or_log_error(
                self.logger,
                package_dicts,
                lambda x: self.parse_has_files(
                    package_dicts=x, existing_relationships=existing_relationships_without_comments
                ),
                [],
            )
        )

        file_dicts: List[Dict] = input_doc_dict.get("files", [])

        # not implemented yet: deal with deprecated fields in file:
        # https://github.com/spdx/tools-python/issues/294 & https://github.com/spdx/tools-python/issues/387
        _ = self.parse_artifact_of(file_dicts=file_dicts)
        _ = self.parse_file_dependencies(file_dicts=file_dicts)

        raise_parsing_error_if_logger_has_messages(self.logger)

        return relationships

    def parse_relationship(self, relationship_dict: Dict) -> Relationship:
        logger = Logger()
        spdx_element_id: Optional[str] = relationship_dict.get("spdxElementId")
        related_spdx_element: Optional[str] = parse_field_or_no_assertion_or_none(
            relationship_dict.get("relatedSpdxElement")
        )
        relationship_type: Optional[RelationshipType] = parse_field_or_log_error(
            logger, relationship_dict.get("relationshipType"), self.parse_relationship_type
        )
        relationship_comment: Optional[str] = relationship_dict.get("comment")
        raise_parsing_error_if_logger_has_messages(logger, "Relationship")

        relationship = construct_or_raise_parsing_error(
            Relationship,
            dict(
                spdx_element_id=spdx_element_id,
                relationship_type=relationship_type,
                related_spdx_element_id=related_spdx_element,
                comment=relationship_comment,
            ),
        )
        return relationship

    @staticmethod
    def parse_relationship_type(relationship_type_str: str) -> RelationshipType:
        try:
            relationship_type = RelationshipType[json_str_to_enum_name(relationship_type_str)]
        except KeyError:
            raise SPDXParsingError([f"Invalid RelationshipType: {relationship_type_str}"])
        return relationship_type

    def parse_document_describes(
        self, doc_spdx_id: str, described_spdx_ids: List[str], existing_relationships: List[Relationship]
    ) -> List[Relationship]:
        logger = Logger()
        describes_relationships = []
        for spdx_id in described_spdx_ids:
            try:
                describes_relationship = Relationship(
                    spdx_element_id=doc_spdx_id,
                    relationship_type=RelationshipType.DESCRIBES,
                    related_spdx_element_id=spdx_id,
                )
            except ConstructorTypeErrors as err:
                logger.append(err.get_messages())
                continue
            if not self.check_if_relationship_exists(describes_relationship, existing_relationships):
                describes_relationships.append(describes_relationship)
        raise_parsing_error_if_logger_has_messages(logger, "document describes relationships")

        return describes_relationships

    def parse_has_files(
        self, package_dicts: List[Dict], existing_relationships: List[Relationship]
    ) -> List[Relationship]:
        # assume existing relationships are stripped of comments
        logger = Logger()
        contains_relationships = []
        for package in package_dicts:
            package_spdx_id: Optional[str] = package.get("SPDXID")
            contained_files: List[str] = delete_duplicates_from_list(package.get("hasFiles", []))
            if not contained_files:
                continue
            for file_spdx_id in contained_files:
                try:
                    contains_relationship = Relationship(
                        spdx_element_id=package_spdx_id,
                        relationship_type=RelationshipType.CONTAINS,
                        related_spdx_element_id=file_spdx_id,
                    )
                except ConstructorTypeErrors as err:
                    logger.append(err.get_messages())
                    continue
                if not self.check_if_relationship_exists(
                    relationship=contains_relationship, existing_relationships=existing_relationships
                ):
                    contains_relationships.append(contains_relationship)
        raise_parsing_error_if_logger_has_messages(logger, "package contains relationships")

        return contains_relationships

    def check_if_relationship_exists(
        self, relationship: Relationship, existing_relationships: List[Relationship]
    ) -> bool:
        # assume existing relationships are stripped of comments
        if relationship in existing_relationships:
            return True
        relationship_inverted: Relationship = self.invert_relationship(relationship)
        if relationship_inverted in existing_relationships:
            return True

        return False

    @staticmethod
    def get_all_relationships_without_comments(existing_relationships: List[Relationship]) -> List[Relationship]:
        relationships_without_comments = [
            Relationship(
                relationship_type=relationship.relationship_type,
                related_spdx_element_id=relationship.related_spdx_element_id,
                spdx_element_id=relationship.spdx_element_id,
            )
            for relationship in existing_relationships
        ]
        return relationships_without_comments

    def invert_relationship(self, relationship: Relationship) -> Relationship:
        return Relationship(
            related_spdx_element_id=relationship.spdx_element_id,
            spdx_element_id=relationship.related_spdx_element_id,
            relationship_type=self.invert_relationship_types[relationship.relationship_type],
            comment=relationship.comment,
        )

    invert_relationship_types = {
        RelationshipType.DESCRIBES: RelationshipType.DESCRIBED_BY,
        RelationshipType.DESCRIBED_BY: RelationshipType.DESCRIBES,
        RelationshipType.CONTAINS: RelationshipType.CONTAINED_BY,
        RelationshipType.CONTAINED_BY: RelationshipType.CONTAINS,
    }

    @staticmethod
    def parse_file_dependencies(file_dicts: List[Dict]) -> List[Relationship]:
        dependency_relationships = []
        # the field fileDependencies is deprecated and should be converted to a relationship
        # https://github.com/spdx/tools-python/issues/387
        return dependency_relationships

    @staticmethod
    def parse_artifact_of(file_dicts: List[Dict]) -> List[Relationship]:
        generated_relationships = []
        # artifactOfs is deprecated and should be converted to an external package and a generated from relationship
        # https://github.com/spdx/tools-python/issues/294
        return generated_relationships
