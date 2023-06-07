# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from beartype.typing import Dict, List, Optional, Union
from license_expression import LicenseExpression

from spdx_tools.spdx.model import Checksum, File, FileType, SpdxNoAssertion, SpdxNone
from spdx_tools.spdx.parser.jsonlikedict.checksum_parser import ChecksumParser
from spdx_tools.spdx.parser.jsonlikedict.dict_parsing_functions import (
    parse_field_or_log_error,
    parse_field_or_no_assertion_or_none,
)
from spdx_tools.spdx.parser.jsonlikedict.license_expression_parser import LicenseExpressionParser
from spdx_tools.spdx.parser.logger import Logger
from spdx_tools.spdx.parser.parsing_functions import (
    construct_or_raise_parsing_error,
    raise_parsing_error_if_logger_has_messages,
)


class FileParser:
    logger: Logger
    checksum_parser: ChecksumParser
    license_expression_parser: LicenseExpressionParser

    def __init__(self):
        self.logger = Logger()
        self.checksum_parser = ChecksumParser()
        self.license_expression_parser = LicenseExpressionParser()

    def parse_file(self, file_dict: Dict) -> Optional[File]:
        logger = Logger()
        name: Optional[str] = file_dict.get("fileName")
        spdx_id: Optional[str] = file_dict.get("SPDXID")
        checksums_list: List[Dict] = file_dict.get("checksums")
        checksums: List[Checksum] = parse_field_or_log_error(
            logger, checksums_list, self.checksum_parser.parse_checksum, field_is_list=True
        )

        attribution_texts: List[str] = file_dict.get("attributionTexts", [])
        comment: Optional[str] = file_dict.get("comment")
        copyright_text: Optional[Union[str, SpdxNoAssertion, SpdxNone]] = parse_field_or_no_assertion_or_none(
            file_dict.get("copyrightText")
        )
        file_contributors: List[str] = file_dict.get("fileContributors", [])
        file_types: List[FileType] = parse_field_or_log_error(
            logger, file_dict.get("fileTypes"), self.parse_file_types
        )

        license_comments: Optional[str] = file_dict.get("licenseComments")

        license_concluded: Optional[Union[LicenseExpression, SpdxNoAssertion, SpdxNone]] = parse_field_or_log_error(
            logger, file_dict.get("licenseConcluded"), self.license_expression_parser.parse_license_expression
        )

        license_info_in_files: List[Union[LicenseExpression, SpdxNoAssertion, SpdxNone]] = parse_field_or_log_error(
            logger,
            file_dict.get("licenseInfoInFiles"),
            self.license_expression_parser.parse_license_expression,
            field_is_list=True,
        )
        notice_text: Optional[str] = file_dict.get("noticeText")
        raise_parsing_error_if_logger_has_messages(logger, "File")

        file = construct_or_raise_parsing_error(
            File,
            dict(
                name=name,
                spdx_id=spdx_id,
                checksums=checksums,
                attribution_texts=attribution_texts,
                comment=comment,
                copyright_text=copyright_text,
                file_types=file_types,
                contributors=file_contributors,
                license_comment=license_comments,
                license_concluded=license_concluded,
                license_info_in_file=license_info_in_files,
                notice=notice_text,
            ),
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
                logger.append(f"Invalid FileType: {file_type}")
                continue
            file_types.append(file_type)
        raise_parsing_error_if_logger_has_messages(logger, "FileType")
        return file_types
