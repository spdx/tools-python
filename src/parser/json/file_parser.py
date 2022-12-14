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
from typing import Dict, List, Optional, Union

from src.model.checksum import Checksum
from src.model.file import File, FileType
from src.model.license_expression import LicenseExpression
from src.model.spdx_no_assertion import SpdxNoAssertion
from src.model.spdx_none import SpdxNone
from src.parser.error import SPDXParsingError
from src.parser.json.checksum_parser import ChecksumParser
from src.parser.json.dict_parsing_functions import parse_optional_field, try_construction_raise_parsing_error
from src.parser.json.license_expression_parser import LicenseExpressionParser
from src.parser.logger import Logger


class FileParser:
    logger: Logger
    checksum_parser: ChecksumParser
    license_expression_parser: LicenseExpressionParser

    def __init__(self):
        self.logger = Logger()
        self.checksum_parser = ChecksumParser()
        self.license_expression_parser = LicenseExpressionParser()

    def parse_files(self, file_dict_list) -> List[File]:
        file_list = []
        for file_dict in file_dict_list:
            try:
                file: File = self.parse_file(file_dict)
                file_list.append(file)
            except SPDXParsingError as err:
                self.logger.append_all(err.get_messages())
                continue
        if self.logger.has_messages():
            raise SPDXParsingError(self.logger.get_messages())
        return file_list

    def parse_file(self, file_dict: Dict) -> Optional[File]:
        logger = Logger()
        name: str = file_dict.get("fileName")
        spdx_id: str = file_dict.get("SPDXID")
        checksums_list: List[Dict] = file_dict.get("checksums")
        try:
            checksums: List[Checksum] = self.checksum_parser.parse_checksums(checksums_list)
        except SPDXParsingError as err:
            logger.append_all(err.get_messages())
            checksums = []

        attribution_texts: Optional[str] = file_dict.get("attributionTexts")
        comment: Optional[str] = file_dict.get("comment")
        copyright_text: Optional[str] = file_dict.get("copyrightText")
        file_contributors: List[str] = file_dict.get("fileContributors")
        try:
            file_types: List[FileType] = parse_optional_field(file_dict.get("fileTypes"), self.parse_file_types)
        except SPDXParsingError as err:
            logger.append_all(err.get_messages())
            file_types = []
        license_comments: Optional[str] = file_dict.get("licenseComments")
        try:
            license_concluded: Optional[Union[LicenseExpression, SpdxNoAssertion, SpdxNone]] = parse_optional_field(
                file_dict.get("licenseConcluded"),
                self.license_expression_parser.parse_license_expression)
        except SPDXParsingError as err:
            logger.append_all(err.get_messages())
            license_concluded = None
        try:
            license_info_in_files: Optional[
                Union[List[LicenseExpression], SpdxNoAssertion, SpdxNone]] = parse_optional_field(
                file_dict.get("licenseInfoInFiles"),
                self.license_expression_parser.parse_license_expression)
        except SPDXParsingError as err:
            logger.append_all(err.get_messages())
            license_info_in_files = None
        notice_text: Optional[str] = file_dict.get("noticeText")

        if logger.has_messages():
            raise SPDXParsingError([f"Error while parsing file {name}: {logger.get_messages()}"])

        file = try_construction_raise_parsing_error(File, dict(name=name, spdx_id=spdx_id, checksums=checksums,
                                                               attribution_texts=attribution_texts,
                                                               comment=comment, copyright_text=copyright_text,
                                                               file_type=file_types, contributors=file_contributors,
                                                               license_comment=license_comments,
                                                               concluded_license=license_concluded,
                                                               license_info_in_file=license_info_in_files,
                                                               notice=notice_text)
                                                    )
        return file

    @staticmethod
    def parse_file_types(file_types_list: List[str]) -> List[FileType]:
        logger = Logger()
        file_types = []
        for file_type in file_types_list:
            try:
                file_type = FileType[file_type]
            except KeyError:
                logger.append(f"FileType {file_type} is not valid.")
                continue
            file_types.append(file_type)
        if logger.has_messages():
            raise SPDXParsingError([f"Error while parsing file_types: {logger.get_messages()}"])
        return file_types
