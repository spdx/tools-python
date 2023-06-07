# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from beartype.typing import Dict

from spdx_tools.spdx.model import Document
from spdx_tools.spdx.parser.error import SPDXParsingError
from spdx_tools.spdx.parser.jsonlikedict.annotation_parser import AnnotationParser
from spdx_tools.spdx.parser.jsonlikedict.creation_info_parser import CreationInfoParser
from spdx_tools.spdx.parser.jsonlikedict.dict_parsing_functions import parse_list_of_elements
from spdx_tools.spdx.parser.jsonlikedict.extracted_licensing_info_parser import ExtractedLicensingInfoParser
from spdx_tools.spdx.parser.jsonlikedict.file_parser import FileParser
from spdx_tools.spdx.parser.jsonlikedict.package_parser import PackageParser
from spdx_tools.spdx.parser.jsonlikedict.relationship_parser import RelationshipParser
from spdx_tools.spdx.parser.jsonlikedict.snippet_parser import SnippetParser
from spdx_tools.spdx.parser.logger import Logger
from spdx_tools.spdx.parser.parsing_functions import (
    construct_or_raise_parsing_error,
    raise_parsing_error_if_logger_has_messages,
)


class JsonLikeDictParser:
    logger: Logger
    creation_info_parser: CreationInfoParser
    package_parser: PackageParser
    file_parser: FileParser
    snippet_parser: SnippetParser
    extracted_licensing_info_parser: ExtractedLicensingInfoParser
    relationship_parser: RelationshipParser
    annotation_parser: AnnotationParser

    def __init__(self):
        self.logger = Logger()
        self.creation_info_parser = CreationInfoParser()
        self.package_parser = PackageParser()
        self.file_parser = FileParser()
        self.snippet_parser = SnippetParser()
        self.extracted_licensing_info_parser = ExtractedLicensingInfoParser()
        self.relationship_parser = RelationshipParser()
        self.annotation_parser = AnnotationParser()

    def parse(self, json_like_dict: Dict) -> Document:
        fields_to_parse = [
            ("creation_info", json_like_dict, self.creation_info_parser.parse_creation_info, False),
            (
                "packages",
                json_like_dict.get("packages"),
                lambda x: parse_list_of_elements(x, self.package_parser.parse_package, self.package_parser.logger),
                True,
            ),
            (
                "files",
                json_like_dict.get("files"),
                lambda x: parse_list_of_elements(x, self.file_parser.parse_file, self.file_parser.logger),
                True,
            ),
            ("annotations", json_like_dict, self.annotation_parser.parse_all_annotations, True),
            (
                "snippets",
                json_like_dict.get("snippets"),
                lambda x: parse_list_of_elements(x, self.snippet_parser.parse_snippet, self.snippet_parser.logger),
                True,
            ),
            ("relationships", json_like_dict, self.relationship_parser.parse_all_relationships, True),
            (
                "extracted_licensing_info",
                json_like_dict.get("hasExtractedLicensingInfos"),
                lambda x: parse_list_of_elements(
                    x,
                    self.extracted_licensing_info_parser.parse_extracted_licensing_info,
                    self.extracted_licensing_info_parser.logger,
                ),
                True,
            ),
        ]

        parsed_fields = {}

        for argument_name, field, parsing_method, optional in fields_to_parse:
            if optional and not field:
                continue
            try:
                parsed_fields[argument_name] = parsing_method(field)
            except SPDXParsingError as err:
                self.logger.extend(err.get_messages())

        raise_parsing_error_if_logger_has_messages(self.logger)

        document = construct_or_raise_parsing_error(Document, parsed_fields)

        return document
