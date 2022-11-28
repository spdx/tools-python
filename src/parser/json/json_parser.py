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

from src.model.document import Document
from src.parser.json.annotation_parser import AnnotationParser
from src.parser.json.creation_info_parser import CreationInfoParser
from src.parser.error import SPDXParsingError
from src.parser.json.extracted_licensing_parser import ExtractedLicensingParser
from src.parser.json.file_parser import FileParser
from src.parser.logger import Logger
from src.parser.json.package_parser import PackageParser
from src.parser.json.relationship_parser import RelationshipParser
from src.parser.json.review_parser import ReviewParser
from src.parser.json.snippet_parser import SnippetParser


class JsonParser:
    logger: Logger
    creation_info_parser: CreationInfoParser
    package_parser: PackageParser
    file_parser: FileParser
    snippet_parser: SnippetParser
    extracted_licenses_parser: ExtractedLicensingParser
    relationship_parser: RelationshipParser
    annotation_parser: AnnotationParser
    review_parser: ReviewParser

    def __init__(self):
        self.logger = Logger()
        self.creation_info_parser = CreationInfoParser(self.logger)
        self.package_parser = PackageParser(self.logger)
        self.file_parser = FileParser(self.logger)
        self.snippet_parser = SnippetParser(self.logger)
        self.extracted_licenses_parser = ExtractedLicensingParser(self.logger)
        self.relationship_parser = RelationshipParser(self.logger)
        self.annotation_parser = AnnotationParser(self.logger)
        self.review_parser = ReviewParser(self.logger)

    def parse(self, filename: str) -> Document:
        logger = Logger()
        with open(filename) as file:
            input_doc_as_dict = json.load(file)
        spdx_version, spdx_id, name, document_namespace, creation_info = self.creation_info_parser.parse(
            input_doc_as_dict)
        document: Document = Document(spdx_version, spdx_id, name, document_namespace, creation_info)

        document.packages = self.package_parser.parse_packages(input_doc_as_dict.get("packages"))
        document.files = self.file_parser.parse_files(input_doc_as_dict.get("files"))
        document.annotations = self.annotation_parser.parse_annotations(input_doc_as_dict.get("annotations"), document.spdx_id)
        document.snippets = self.snippet_parser.parse_snippets(input_doc_as_dict.get("snippets"))
        document.relationships = self.relationship_parser.parse_relationships(input_doc_as_dict.get("relationships"))
        review_to_annotations = self.review_parser.parse_reviews(input_doc_as_dict.get("revieweds"))
        for annotation in review_to_annotations:
            document.annotations.append(annotation)

        document.extracted_licensing_info = map(self.extracted_licenses_parser.parse_extracted_licensing_info,
                                                input_doc_as_dict.get("hasExtractedLicensingInfo"))

        if logger.has_errors():
            raise SPDXParsingError(logger.get_errors())
        return document
