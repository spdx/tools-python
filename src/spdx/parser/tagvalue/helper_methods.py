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
import re
from typing import Optional, Callable, Any, Dict

from ply.yacc import YaccProduction

from spdx.casing_tools import camel_case_to_snake_case
from spdx.model.annotation import Annotation
from spdx.model.checksum import Checksum, ChecksumAlgorithm
from spdx.model.document import CreationInfo
from spdx.model.extracted_licensing_info import ExtractedLicensingInfo
from spdx.model.file import File
from spdx.model.package import Package
from spdx.model.snippet import Snippet
from spdx.parser.error import SPDXParsingError


def grammar_rule(doc):
    # this is a helper method to use decorators for the parsing methods instead of docstrings
    def decorate(func):
        func.__doc__ = doc
        return func

    return decorate


def str_from_text(text: Optional[str]) -> Optional[str]:
    regex = re.compile("<text>((.|\n)+)</text>", re.UNICODE)
    match = regex.match(text)
    if match:
        return match.group(1)
    elif isinstance(text, str):
        return text
    else:
        return None


def parse_checksum(checksum_str: str) -> Checksum:
    # The lexer and the corresponding regex for the token CHECKSUM and EXT_DOC_REF_CHECKSUM ensure that the passed
    # checksum_str is formatted in the way that the following lines of code can't cause an error.
    algorithm, value = checksum_str.split(":")
    algorithm = ChecksumAlgorithm[algorithm.upper().replace("-", "_")]
    value = value.strip()
    checksum = Checksum(algorithm, value)
    return checksum


def set_value(parsed_value: YaccProduction, dict_to_fill: Dict[str, Any], argument_name: Optional[str] = None,
              method_to_apply: Callable = lambda x: x):
    if not argument_name:
        argument_name = get_property_name(parsed_value[1])
    if argument_name in dict_to_fill:
        dict_to_fill["logger"].append(
            f"Multiple values for {parsed_value[1]} found. Line: {parsed_value.lineno(1)}")
        return
    try:
        dict_to_fill[argument_name] = method_to_apply(parsed_value[2])
    except SPDXParsingError as err:
        dict_to_fill["logger"].append(err.get_messages())
    except ValueError as err:
        dict_to_fill["logger"].append(err.args[0])
    except KeyError:
        dict_to_fill["logger"].append(f"Invalid {parsed_value[1]}: {parsed_value[2]}. Line: {parsed_value.lineno(1)}")


def get_property_name(tag: str):
    if tag not in TAG_DATA_MODEL_FIELD.keys():
        return camel_case_to_snake_case(tag)
    return TAG_DATA_MODEL_FIELD[tag][1]


# This dictionary serves as a mapping from a tag to the corresponding class and field in the internal data model.
# This mapping is not complete as we only list the values which can be parsed by a generic method and don't need any
# individual logic.
TAG_DATA_MODEL_FIELD = {
    "SPDXVersion": (CreationInfo, "spdx_version"), "DataLicense": (CreationInfo, "data_license"),
    "DocumentName": (CreationInfo, "name"), "DocumentComment": (CreationInfo, "document_comment"),
    "DocumentNamespace": (CreationInfo, "document_namespace"), "Creator": (CreationInfo, "creator"),
    "Created": (CreationInfo, "created"), "CreatorComment": (CreationInfo, "creator_comment"),
    "LicenseListVersion": (CreationInfo, "license_list_version"),
    "ExternalDocumentRef": (CreationInfo, "external_document_refs"),
    "FileName": (File, "name"), "FileType": (File, "file_type"), "FileChecksum": (File, "checksums"),
    "FileNotice": (File, "notice"), "FileCopyrightText": (File, "copyright_text"),
    "LicenseComments": (File, "license_comment"), "FileComment": (File, "comment"),
    "LicenseConcluded": (File, "license_concluded"), "LicenseDeclared": (File, "license_declared"),
    "PackageName": (Package, "name"), "PackageComment": (Package, "comment"),
    "PackageCopyrightText": (Package, "copyright_text"), "PackageLicenseComments": (Package, "license_comment"),
    "PackageLicenseDeclared": (Package, "license_declared"), "PackageLicenseConcluded": (Package, "license_concluded"),
    "PackageFileName": (Package, "file_name"), "PackageVersion": (Package, "version"),
    "PackageDownloadLocation": (Package, "download_location"), "PackageSummary": (Package, "summary"),
    "PackageSourceInfo": (Package, "source_info"), "PackageSupplier": (Package, "supplier"),
    "PackageOriginator": (Package, "originator"), "PackageDescription": (Package, "description"),
    "PackageHomePage": (Package, "homepage"),
    "SnippetSPDXID": (Snippet, "spdx_id"), "SnippetFromFileSPDXID": (Snippet, "file_spdx_id"),
    "SnippetName": (Snippet, "name"),
    "SnippetComment": (Snippet, "comment"), "SnippetCopyrightText": (Snippet, "copyright_text"),
    "SnippetLicenseComments": (Snippet, "license_comment"), "SnippetLicenseConcluded": (Snippet, "license_concluded"),
    "SnippetByteRange": (Snippet, "byte_range"), "SnippetLineRange": (Snippet, "line_range"),
    "Annotator": (Annotation, "annotator"),
    "SPDXREF": (Annotation, "spdx_id"), "AnnotationComment": (Annotation, "annotation_comment"),
    "LicenseID": (ExtractedLicensingInfo, "license_id"), "ExtractedText": (ExtractedLicensingInfo, "extracted_text"),
    "LicenseComment": (ExtractedLicensingInfo, "comment"), "LicenseName": (ExtractedLicensingInfo, "license_name")
}
