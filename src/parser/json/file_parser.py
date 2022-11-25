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

from src.model.file import File, FileType
from src.model.typing.constructor_type_errors import ConstructorTypeErrors
from src.parser.error import SPDXParsingError
from src.parser.json.checksum_parser import ChecksumParser
from src.parser.json.dict_parsing_functions import parse_license_expression, parse_optional_field
from src.parser.logger import Logger


class FileParser:
    logger: Logger
    checksum_parser: ChecksumParser

    def __init__(self):
        self.logger = Logger()
        self.checksum_parser = ChecksumParser()

    def parse_file(self, file_dict: Dict) -> Optional[File]:
        name = file_dict.get("fileName")
        spdx_id = file_dict.get("SPDXID")
        try:
            checksums = self.checksum_parser.parse_checksums(file_dict.get("checksums"))
        except SPDXParsingError as err:
            self.logger.append_all(err.get_messages())
            checksums = []

        attribution_texts = file_dict.get("attributionTexts")
        comment = file_dict.get("comment")
        copyright_text = file_dict.get("copyrightText")
        file_contributors = file_dict.get("fileContributors")

        file_types = parse_optional_field(file_dict.get("fileTypes"), self.parse_file_types)

        license_comments = file_dict.get("licenseComments")
        try:
            license_concluded = parse_optional_field(file_dict.get("licenseConcluded"), parse_license_expression)
        except ConstructorTypeErrors as err:
            self.logger.append_all(err.get_messages())
            license_concluded = []
        try:
            license_info_in_files = parse_optional_field(file_dict.get("licenseInfoInFiles"), parse_license_expression)
        except ConstructorTypeErrors as err:
            self.logger.append_all(err.get_messages())
            license_info_in_files = []
        notice_text = file_dict.get("noticeText")

        if self.logger.has_messages():
            raise SPDXParsingError(self.logger.get_messages())

        try:
            file = File(name=name, spdx_id=spdx_id, checksums=checksums, attribution_texts=attribution_texts, comment=comment, copyright_text=copyright_text,
                        file_type=file_types, contributors=file_contributors, license_comment=license_comments,
                        concluded_license=license_concluded, license_info_in_file=license_info_in_files, notice=notice_text)
        except ConstructorTypeErrors as error:
            self.logger.append_all(error.get_messages())
            raise SPDXParsingError(self.logger.get_messages())

        return file

    def parse_files(self, file_dict_list) -> List[File]:
        file_list = []
        for file_dict in file_dict_list:
            try:
                file = self.parse_file(file_dict)
                file_list.append(file)
            except SPDXParsingError:
              #  self.logger.append_all(err.get_messages())
                continue
        if self.logger.has_messages():
            raise SPDXParsingError(self.logger.get_messages())
        return file_list

    def parse_file_types(self, file_types_list: List[str]) -> List[FileType]:
        file_types = []
        for file_type in file_types_list:
            try:
                file_type = FileType[file_type]
            except KeyError:
                self.logger.append(f"FileType {file_type} is not valid.")
                continue
            file_types.append(file_type)

        return file_types
