# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from enum import Enum, auto

from beartype.typing import Dict, List, Optional, Tuple, Union
from license_expression import LicenseExpression

from spdx_tools.spdx.model import Snippet, SpdxNoAssertion, SpdxNone
from spdx_tools.spdx.parser.error import SPDXParsingError
from spdx_tools.spdx.parser.jsonlikedict.dict_parsing_functions import (
    parse_field_or_log_error,
    parse_field_or_no_assertion_or_none,
)
from spdx_tools.spdx.parser.jsonlikedict.license_expression_parser import LicenseExpressionParser
from spdx_tools.spdx.parser.logger import Logger
from spdx_tools.spdx.parser.parsing_functions import construct_or_raise_parsing_error


class RangeType(Enum):
    BYTE = auto()
    LINE = auto()


class SnippetParser:
    logger: Logger
    license_expression_parser = LicenseExpressionParser

    def __init__(self):
        self.logger = Logger()
        self.license_expression_parser = LicenseExpressionParser()

    def parse_snippet(self, snippet_dict: Dict) -> Snippet:
        logger = Logger()
        spdx_id: Optional[str] = snippet_dict.get("SPDXID")
        file_spdx_id: Optional[str] = snippet_dict.get("snippetFromFile")
        name: Optional[str] = snippet_dict.get("name")

        ranges: Dict = parse_field_or_log_error(logger, snippet_dict.get("ranges", []), self.parse_ranges, default={})
        byte_range: Optional[Tuple[Union[int, str], Union[int, str]]] = ranges.get(RangeType.BYTE)
        line_range: Optional[Tuple[Union[int, str], Union[int, str]]] = ranges.get(RangeType.LINE)
        byte_range = self.convert_range_from_str(byte_range)
        line_range = self.convert_range_from_str(line_range)

        attribution_texts: List[str] = snippet_dict.get("attributionTexts", [])
        comment: Optional[str] = snippet_dict.get("comment")
        copyright_text: Optional[Union[str, SpdxNoAssertion, SpdxNone]] = parse_field_or_no_assertion_or_none(
            snippet_dict.get("copyrightText")
        )
        license_comment: Optional[str] = snippet_dict.get("licenseComments")
        license_concluded: Optional[Union[LicenseExpression, SpdxNoAssertion, SpdxNone]] = parse_field_or_log_error(
            logger, snippet_dict.get("licenseConcluded"), self.license_expression_parser.parse_license_expression
        )

        license_info: List[Union[LicenseExpression], SpdxNoAssertion, SpdxNone] = parse_field_or_log_error(
            logger,
            snippet_dict.get("licenseInfoInSnippets"),
            self.license_expression_parser.parse_license_expression,
            field_is_list=True,
        )
        if logger.has_messages():
            raise SPDXParsingError([f"Error while parsing snippet: {logger.get_messages()}"])

        snippet = construct_or_raise_parsing_error(
            Snippet,
            dict(
                spdx_id=spdx_id,
                name=name,
                byte_range=byte_range,
                file_spdx_id=file_spdx_id,
                line_range=line_range,
                attribution_texts=attribution_texts,
                comment=comment,
                copyright_text=copyright_text,
                license_comment=license_comment,
                license_concluded=license_concluded,
                license_info_in_snippet=license_info,
            ),
        )

        return snippet

    def parse_ranges(self, ranges_from_snippet: List[Dict]) -> Dict:
        logger = Logger()
        ranges = {}
        for range_dict in ranges_from_snippet:
            try:
                range_type: RangeType = self.validate_range_and_get_type(range_dict)
                start_end_tuple: Tuple[int, int] = SnippetParser.get_start_end_tuple(range_dict, range_type)
                ranges[range_type] = start_end_tuple
            except ValueError as error:
                logger.append(error.args[0])
        if logger.has_messages():
            raise SPDXParsingError([f"Error while parsing snippet ranges: {logger.get_messages()}"])
        return ranges

    @staticmethod
    def get_start_end_tuple(range_dict: Dict, range_type: RangeType) -> Tuple[int, int]:
        end_pointer: Dict = range_dict["endPointer"]
        start_pointer: Dict = range_dict["startPointer"]
        if range_type == RangeType.BYTE:
            start: int = start_pointer["offset"]
            end: int = end_pointer["offset"]
        else:
            start: int = start_pointer["lineNumber"]
            end: int = end_pointer["lineNumber"]
        return start, end

    def validate_range_and_get_type(self, range_dict: Dict) -> RangeType:
        if "startPointer" not in range_dict:
            raise ValueError("Startpointer missing in snippet ranges.")
        if "endPointer" not in range_dict:
            raise ValueError("Endpointer missing in snippet ranges.")
        start_pointer_type: RangeType = self.validate_pointer_and_get_type(range_dict["startPointer"])
        end_pointer_type: RangeType = self.validate_pointer_and_get_type(range_dict["endPointer"])
        if start_pointer_type != end_pointer_type:
            raise ValueError("Type of startpointer is not the same as type of endpointer.")
        return start_pointer_type

    @staticmethod
    def validate_pointer_and_get_type(pointer: Dict) -> RangeType:
        if "offset" in pointer and "lineNumber" in pointer:
            raise ValueError('Couldn\'t determine type of pointer: "offset" and "lineNumber" provided as key.')
        if "offset" not in pointer and "lineNumber" not in pointer:
            raise ValueError('Couldn\'t determine type of pointer: neither "offset" nor "lineNumber" provided as key.')
        return RangeType.BYTE if "offset" in pointer else RangeType.LINE

    @staticmethod
    def convert_range_from_str(
        _range: Tuple[Union[int, str], Union[int, str]]
    ) -> Tuple[Union[int, str], Union[int, str]]:
        # XML does not support integers, so we have to convert from string (if possible)
        if not _range:
            return _range

        if isinstance(_range[0], str) and _range[0].isdigit():
            _range = int(_range[0]), _range[1]
        if isinstance(_range[1], str) and _range[1].isdigit():
            _range = _range[0], int(_range[1])
        return _range
