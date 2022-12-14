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
import json
from json import JSONDecodeError
from typing import List

from src.model.document import Document, CreationInfo
from src.model.package import Package
from src.parser.json.annotation_parser import AnnotationParser
from src.parser.json.creation_info_parser import CreationInfoParser
from src.parser.error import SPDXParsingError
from src.parser.json.dict_parsing_functions import try_construction_raise_parsing_error, \
    try_parse_optional_field_append_logger_when_failing, try_parse_required_field_append_logger_when_failing
from src.parser.json.extracted_licensing_parser import ExtractedLicensingInfoParser
from src.parser.json.file_parser import FileParser
from src.parser.logger import Logger
from src.parser.json.package_parser import PackageParser
from src.parser.json.relationship_parser import RelationshipParser
from src.parser.json.snippet_parser import SnippetParser


class JsonParser:
    logger: Logger
    creation_info_parser: CreationInfoParser
    package_parser: PackageParser
    file_parser: FileParser
    snippet_parser: SnippetParser
    extracted_licenses_parser: ExtractedLicensingInfoParser
    relationship_parser: RelationshipParser
    annotation_parser: AnnotationParser

    def __init__(self):
        self.logger = Logger()
        self.creation_info_parser = CreationInfoParser()
        self.package_parser = PackageParser()
        self.file_parser = FileParser()
        self.snippet_parser = SnippetParser()
        self.extracted_licenses_parser = ExtractedLicensingInfoParser()
        self.relationship_parser = RelationshipParser()
        self.annotation_parser = AnnotationParser()

    def parse(self, filename: str) -> Document:
        try:
            with open(filename) as file:
                input_doc_as_dict = json.load(file)
        except FileNotFoundError:
            self.logger.append(f"File {filename} not found.")
            raise SPDXParsingError(self.logger.get_messages())
        except JSONDecodeError:
            self.logger.append(f"File {filename} is not a valid JSON file.")
            raise SPDXParsingError(self.logger.get_messages())

        creation_info: CreationInfo = try_parse_required_field_append_logger_when_failing(logger=self.logger,
                                                                                          field=input_doc_as_dict,
                                                                                          method_to_parse=self.creation_info_parser.parse_creation_info)

        packages: List[Package] = try_parse_optional_field_append_logger_when_failing(logger=self.logger,
                                                                                      field=input_doc_as_dict.get(
                                                                                          "packages"),
                                                                                      method_to_parse=self.package_parser.parse_packages,
                                                                                      default=None)

        files = try_parse_optional_field_append_logger_when_failing(logger=self.logger,
                                                                    field=input_doc_as_dict.get("files"),
                                                                    method_to_parse=self.file_parser.parse_files)

        annotations = try_parse_optional_field_append_logger_when_failing(logger=self.logger,
                                                                          field=input_doc_as_dict,
                                                                          method_to_parse=self.annotation_parser.parse_all_annotations)
        snippets = try_parse_optional_field_append_logger_when_failing(logger=self.logger,
                                                                       field=input_doc_as_dict.get("snippets"),
                                                                       method_to_parse=self.snippet_parser.parse_snippets)
        relationships = try_parse_optional_field_append_logger_when_failing(logger=self.logger,
                                                                            field=input_doc_as_dict,
                                                                            method_to_parse=self.relationship_parser.parse_all_relationships)
        extracted_licensing_info = try_parse_optional_field_append_logger_when_failing(logger=self.logger,
                                                                                       field=input_doc_as_dict.get(
                                                                                           "hasExtractedLicensingInfos"),
                                                                                       method_to_parse=self.extracted_licenses_parser.parse_extracted_licensing_infos)

        if self.logger.has_messages():
            raise SPDXParsingError(self.logger.get_messages())

        document = try_construction_raise_parsing_error(Document, dict(creation_info=creation_info, packages=packages,
                                                                       files=files,
                                                                       annotations=annotations,
                                                                       snippets=snippets, relationships=relationships,
                                                                       extracted_licensing_info=extracted_licensing_info))

        return document
