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
from typing import Dict, Tuple

from src.model.snippet import Snippet
from src.parser.annotationparser import AnnotationParser
from src.parser.logger import Logger


class SnippetParser:
    annotation_parser: AnnotationParser
    logger: Logger

    def __init__(self, logger: Logger):
        self.annotation_parser = AnnotationParser()
        self.logger = logger

    def parse_ranges(self, ranges: Dict) -> Tuple:
        byte_range = ()
        line_range = ()
        return byte_range, line_range

    def parse(self, snippet_dict: Dict) -> Snippet:
        spdx_id = snippet_dict.get("SPDXID")
        file_spdx_id = snippet_dict.get("snippetFromFile")
        name = snippet_dict.get("name")
        byte_range, line_range = self.parse_ranges(snippet_dict.get("ranges"))
        snippet = Snippet(spdx_id, file_spdx_id, byte_range, name)
        if line_range:
            snippet.line_range = line_range
        if "attributionTexts" in snippet_dict:
            attribution_texts = [attribution_text for attribution_text in snippet_dict.get("attributionTexts")]
            snippet.attribution_texts = attribution_texts
        if "comment" in snippet_dict:
            comment = snippet_dict.get("comment")
            snippet.comment = comment
        if "copyrightText" in snippet_dict:
            copyright_text = snippet_dict.get("copyrightText")
            snippet.copyright_text = copyright_text
        if "license_comments" in snippet_dict:
            license_comment = snippet_dict.get("licenseComments")
            snippet.license_comment = license_comment
        if "licenseConcluded" in snippet_dict: #LicenseExpression?
            concluded_license = snippet_dict.get("licenseConcluded")
            snippet.concluded_license = concluded_license
        if "licenInfoInSnippets" in snippet_dict: #LicenseExpression?
            license_infos = [license_info for license_info in snippet_dict.get("licenseInfoInSnippets")]
            snippet.license_info = license_infos
        if "annotations" in snippet_dict:
            self.annotation_parser.parse(snippet_dict.get("annotations"), snippet.spdx_id)

        return snippet
