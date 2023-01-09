# Copyright (c) 2023 spdx contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from typing import Dict, Any

import xmltodict

from spdx.model.document import Document
from spdx.parser.error import SPDXParsingError
from spdx.parser.jsonlikedict.json_like_dict_parser import JsonLikeDictParser


LIST_LIKE_FIELDS = [
    "creators",
    "externalDocumentRefs",
    "hasExtractedLicensingInfos",
    "seeAlsos",
    "annotations",
    "relationships",
    "snippets",
    "reviewers",
    "fileTypes",
    "licenseInfoFromFiles",
    "licenseInfoInFiles",
    "artifactOf",
    "fileContributors",
    "fileDependencies",
    "files",
    "documentDescribes",
    "packages",
    "checksums",
    "hasFiles",
    "externalRefs",
    "ranges",
    "licenseInfoInSnippets",
    "packageVerificationCodeExcludedFiles",
    "attributionTexts"
    ]


def parse_from_file(file_name: str) -> Document:
    with open(file_name) as file:
        parsed_xml: Dict = xmltodict.parse(file.read(), encoding="utf-8")

    input_doc_as_dict: Dict = _fix_list_like_fields(parsed_xml).get("Document")

    if not input_doc_as_dict:
        raise SPDXParsingError(['Did not find the XML top level tag "Document".'])

    return JsonLikeDictParser().parse(input_doc_as_dict)


def _fix_list_like_fields(data: Any) -> Any:
    """
    XML files do not contain lists. Thus, single fields that should be a list in SPDX have to be manually cast.
    This method takes a parsed dictionary and converts all values with key from LIST_LIKE_FIELDS to lists.
    """
    if isinstance(data, dict):
        new_data = {}
        for key, value in data.items():
            if key in LIST_LIKE_FIELDS and not isinstance(value, list):
                new_data[key] = [_fix_list_like_fields(value)]
            else:
                new_data[key] = _fix_list_like_fields(value)
        return new_data

    if isinstance(data, list):
        new_data = []
        for element in data:
            new_data.append(_fix_list_like_fields(element))
        return new_data

    return data
