# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import xmltodict
from beartype.typing import Any, Dict

from spdx_tools.spdx.model import Document
from spdx_tools.spdx.parser.error import SPDXParsingError
from spdx_tools.spdx.parser.jsonlikedict.json_like_dict_parser import JsonLikeDictParser

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
    "attributionTexts",
]


def parse_from_file(file_name: str, encoding: str = "utf-8") -> Document:
    with open(file_name, encoding=encoding) as file:
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
                new_data[key] = [_fix_list_like_fields(value)] if value else []
            else:
                new_data[key] = _fix_list_like_fields(value)
        return new_data

    if isinstance(data, list):
        new_data = []
        for element in data:
            new_data.append(_fix_list_like_fields(element))
        return new_data

    return data
