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
from enum import auto, Enum
from typing import Dict, Tuple, List

from src.model.snippet import Snippet
from src.parser.json.annotation_parser import AnnotationParser

from src.parser.json.parser_utils import set_optional_property
from src.parser.logger import Logger


class RangeType(Enum):
    BYTE = auto()
    LINE = auto()


class SnippetParser:
    annotation_parser: AnnotationParser
    logger: Logger

    def __init__(self, logger: Logger):
        self.annotation_parser = AnnotationParser(logger)
        self.logger = logger

    def parse_snippets(self, snippet_dicts_list: List[Dict]) -> List[Snippet]:
        snippets_list = []
        for snippet_dict in snippet_dicts_list:
            snippets_list.append(self.parse_snippet(snippet_dict))
        return snippets_list

    def parse_snippet(self, snippet_dict: Dict) -> Snippet:
        spdx_id = snippet_dict.get("SPDXID")
        file_spdx_id = snippet_dict.get("snippetFromFile")
        name = snippet_dict.get("name")
        ranges= self.parse_ranges(snippet_dict.get("ranges"))
        snippet = Snippet(spdx_id, file_spdx_id, ranges[RangeType.BYTE], name)

        snippet.line_range = set_optional_property(RangeType.LINE, ranges)
        snippet.attribution_texts = set_optional_property("attributionTexts", snippet_dict)
        snippet.comment = set_optional_property("comment", snippet_dict)
        snippet.copyright_text = set_optional_property("copyrightText", snippet_dict)
        snippet.license_comment = set_optional_property("licenseComments", snippet_dict)
        snippet.concluded_license = set_optional_property("licenseConcluded", snippet_dict)
        snippet.license_info = set_optional_property("licenseInfoInSnippets", snippet_dict)

        if "annotations" in snippet_dict:
            self.annotation_parser.parse_annotation(snippet_dict.get("annotations"), snippet.spdx_id)

        return snippet

    def parse_ranges(self, ranges_from_snippet: List[Dict]) -> Dict:
        ranges = {}
        for range_dict in ranges_from_snippet:
            try:
                range_type = self.validate_range_and_get_type(range_dict)
                start_end_tuple: Tuple[int, int] = SnippetParser.get_start_end_tuple(range_dict, range_type)
                ranges[range_type] = start_end_tuple
            except ValueError as error:
                self.logger.append(error.args[0])
        return ranges

    @staticmethod
    def get_start_end_tuple(range_dict: Dict, range_type: RangeType) -> Tuple[int, int]:
        end_pointer = range_dict["endPointer"]
        start_pointer = range_dict["startPointer"]
        if range_type == RangeType.BYTE:
            start = int(start_pointer["offset"])
            end = int(end_pointer["offset"])
        else:
            start = int(start_pointer["lineNumber"])
            end = int(end_pointer["lineNumber"])

        return start, end

    def validate_range_and_get_type(self, range_dict: Dict) -> RangeType:
        if ("startPointer" not in range_dict) or ("endPointer" not in range_dict):
            raise ValueError("Snippet::ranges")
        start_pointer_type = self.validate_pointer_and_get_type(range_dict["startPointer"])
        end_pointer_type = self.validate_pointer_and_get_type(range_dict["endPointer"])
        if start_pointer_type != end_pointer_type:
            raise ValueError("Snippet::ranges")
        return start_pointer_type

    @staticmethod
    def validate_pointer_and_get_type(self, pointer: Dict) -> RangeType:
        if ("offset" in pointer and "lineNumber" in pointer) or (
                "offset" not in pointer and "lineNumber" not in pointer):
            raise ValueError("Snippet::ranges")
        return RangeType.BYTE if "offset" in pointer else RangeType.LINE
