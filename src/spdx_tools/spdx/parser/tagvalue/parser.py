# Copyright (c) 2014 Ahmed H. Ismail
# Copyright (c) 2023 spdx contributors
# SPDX-License-Identifier: Apache-2.0
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

from beartype.typing import Any, Dict, List
from license_expression import ExpressionError, get_spdx_licensing
from ply import yacc
from ply.yacc import LRParser

from spdx_tools.spdx.datetime_conversions import datetime_from_str
from spdx_tools.spdx.model import (
    Annotation,
    AnnotationType,
    CreationInfo,
    Document,
    ExternalDocumentRef,
    ExternalPackageRef,
    ExternalPackageRefCategory,
    ExtractedLicensingInfo,
    File,
    FileType,
    Package,
    PackagePurpose,
    PackageVerificationCode,
    Relationship,
    RelationshipType,
    Snippet,
    SpdxNoAssertion,
    SpdxNone,
    Version,
)
from spdx_tools.spdx.parser.actor_parser import ActorParser
from spdx_tools.spdx.parser.error import SPDXParsingError
from spdx_tools.spdx.parser.logger import Logger
from spdx_tools.spdx.parser.parsing_functions import (
    construct_or_raise_parsing_error,
    raise_parsing_error_if_logger_has_messages,
)
from spdx_tools.spdx.parser.tagvalue.helper_methods import (
    TAG_DATA_MODEL_FIELD,
    grammar_rule,
    parse_checksum,
    set_value,
    str_from_text,
)
from spdx_tools.spdx.parser.tagvalue.lexer import SPDXLexer

CLASS_MAPPING = dict(
    File="files",
    Annotation="annotations",
    Relationship="relationships",
    Snippet="snippets",
    Package="packages",
    ExtractedLicensingInfo="extracted_licensing_info",
)
ELEMENT_EXPECTED_START_TAG = dict(
    File="FileName",
    Annotation="Annotator",
    Relationship="Relationship",
    Snippet="SnippetSPDXID",
    Package="PackageName",
    ExtractedLicensingInfo="LicenseID",
)


class Parser:
    tokens: List[str]
    logger: Logger
    current_element: Dict[str, Any]
    creation_info: Dict[str, Any]
    elements_built: Dict[str, Any]
    lex: SPDXLexer
    yacc: LRParser

    def __init__(self, **kwargs):
        self.tokens = SPDXLexer.tokens
        self.logger = Logger()
        self.current_element = {"logger": Logger()}
        self.creation_info = {"logger": Logger()}
        self.elements_built = dict()
        self.lex = SPDXLexer()
        self.lex.build(reflags=re.UNICODE)
        self.yacc = yacc.yacc(module=self, **kwargs)

    @grammar_rule("start : start attrib ")
    def p_start_start_attrib(self, p):
        pass

    @grammar_rule("start : attrib ")
    def p_start_attrib(self, p):
        pass

    @grammar_rule(
        "attrib : spdx_version\n| spdx_id\n| data_license\n| doc_name\n| document_comment\n| document_namespace\n| "
        "creator\n| created\n| creator_comment\n| license_list_version\n| ext_doc_ref\n"
        # attributes for file
        "| file_name\n| file_type\n| file_checksum\n| file_license_concluded\n| file_license_info\n"
        "| file_copyright_text\n| file_license_comment\n| file_attribution_text\n| file_notice\n| file_comment\n"
        "| file_contributor\n"
        # attributes for annotation
        "| annotator\n| annotation_date\n| annotation_comment\n| annotation_type\n| annotation_spdx_id\n"
        # attributes for relationship
        "| relationship\n"
        # attributes for snippet
        "| snippet_spdx_id\n| snippet_name\n| snippet_comment\n| snippet_attribution_text\n| snippet_copyright_text\n"
        "| snippet_license_comment\n| file_spdx_id\n| snippet_license_concluded\n| snippet_license_info\n"
        "| snippet_byte_range\n| snippet_line_range\n"
        # attributes for package
        "| package_name\n| package_version\n| download_location\n| files_analyzed\n| homepage\n"
        "| summary\n| source_info\n| pkg_file_name\n| supplier\n| originator\n| pkg_checksum\n"
        "| verification_code\n| description\n| pkg_comment\n| pkg_attribution_text\n| pkg_license_declared\n"
        "| pkg_license_concluded\n| pkg_license_info\n| pkg_license_comment\n| pkg_copyright_text\n"
        "| pkg_external_ref\n| primary_package_purpose\n| built_date\n| release_date\n| valid_until_date\n"
        # attributes for extracted licensing info
        "| license_id\n| extracted_text\n| license_name\n| license_cross_ref\n| lic_comment\n"
        "| unknown_tag "
    )
    def p_attrib(self, p):
        pass

    # general parsing methods
    @grammar_rule(
        "license_id : LICENSE_ID error\n license_cross_ref : LICENSE_CROSS_REF error\n "
        "lic_comment : LICENSE_COMMENT error\n license_name : LICENSE_NAME error\n "
        "extracted_text : LICENSE_TEXT error\n "
        "file_name : FILE_NAME error\n file_contributor : FILE_CONTRIBUTOR error\n "
        "file_notice : FILE_NOTICE error\n file_copyright_text : FILE_COPYRIGHT_TEXT error\n "
        "file_license_comment : FILE_LICENSE_COMMENT error\n "
        "file_license_info : FILE_LICENSE_INFO error\n file_comment : FILE_COMMENT error\n "
        "file_checksum : FILE_CHECKSUM error\n file_license_concluded : FILE_LICENSE_CONCLUDED error\n "
        "file_type : FILE_TYPE error\n file_attribution_text : FILE_ATTRIBUTION_TEXT error\n "
        "package_name : PKG_NAME error\n pkg_attribution_text : PKG_ATTRIBUTION_TEXT error\n "
        "description : PKG_DESCRIPTION error\n pkg_comment : PKG_COMMENT error\n "
        "summary : PKG_SUMMARY error\n pkg_copyright_text : PKG_COPYRIGHT_TEXT error\n "
        "pkg_external_ref : PKG_EXTERNAL_REF error\n pkg_license_comment : PKG_LICENSE_COMMENT error\n "
        "pkg_license_declared : PKG_LICENSE_DECLARED error\n pkg_license_info : PKG_LICENSE_INFO error \n "
        "pkg_license_concluded : PKG_LICENSE_CONCLUDED error\n source_info : PKG_SOURCE_INFO error\n "
        "homepage : PKG_HOMEPAGE error\n pkg_checksum : PKG_CHECKSUM error\n "
        "verification_code : PKG_VERIFICATION_CODE error\n originator : PKG_ORIGINATOR error\n "
        "download_location : PKG_DOWNLOAD_LOCATION error\n files_analyzed : PKG_FILES_ANALYZED error\n "
        "supplier : PKG_SUPPLIER error\n pkg_file_name : PKG_FILE_NAME error\n "
        "package_version : PKG_VERSION error\n primary_package_purpose : PRIMARY_PACKAGE_PURPOSE error\n "
        "built_date : BUILT_DATE error\n release_date : RELEASE_DATE error\n "
        "valid_until_date : VALID_UNTIL_DATE error\n snippet_spdx_id : SNIPPET_SPDX_ID error\n "
        "snippet_name : SNIPPET_NAME error\n snippet_comment : SNIPPET_COMMENT error\n "
        "snippet_attribution_text : SNIPPET_ATTRIBUTION_TEXT error\n "
        "snippet_copyright_text : SNIPPET_COPYRIGHT_TEXT error\n "
        "snippet_license_comment : SNIPPET_LICENSE_COMMENT error\n file_spdx_id : SNIPPET_FILE_SPDXID error\n "
        "snippet_license_concluded : SNIPPET_LICENSE_CONCLUDED error\n "
        "snippet_license_info : SNIPPET_LICENSE_INFO error\n "
        "snippet_byte_range : SNIPPET_BYTE_RANGE error\n snippet_line_range : SNIPPET_LINE_RANGE error\n "
        "annotator : ANNOTATOR error\n annotation_date : ANNOTATION_DATE error\n "
        "annotation_comment : ANNOTATION_COMMENT error\n annotation_type : ANNOTATION_TYPE error\n "
        "annotation_spdx_id : ANNOTATION_SPDX_ID error\n relationship : RELATIONSHIP error"
    )
    def p_current_element_error(self, p):
        if p[1] in ELEMENT_EXPECTED_START_TAG.values():
            self.initialize_new_current_element(TAG_DATA_MODEL_FIELD[p[1]][0])
        self.current_element["logger"].append(
            f"Error while parsing {p[1]}: Token did not match specified grammar rule. Line: {p.lineno(1)}"
        )

    @grammar_rule(
        "license_name : LICENSE_NAME line_or_no_assertion\n extracted_text : LICENSE_TEXT text_or_line\n "
        "lic_comment : LICENSE_COMMENT text_or_line\n license_id : LICENSE_ID LINE\n "
        "file_name : FILE_NAME LINE \n file_notice : FILE_NOTICE text_or_line\n "
        "file_copyright_text : FILE_COPYRIGHT_TEXT line_or_no_assertion_or_none\n "
        "file_license_comment : FILE_LICENSE_COMMENT text_or_line\n "
        "file_comment : FILE_COMMENT text_or_line\n "
        "file_license_concluded : FILE_LICENSE_CONCLUDED license_or_no_assertion_or_none\n "
        "package_name : PKG_NAME LINE\n description : PKG_DESCRIPTION text_or_line\n "
        "summary : PKG_SUMMARY text_or_line\n source_info : PKG_SOURCE_INFO text_or_line\n "
        "homepage : PKG_HOMEPAGE line_or_no_assertion_or_none\n "
        "download_location : PKG_DOWNLOAD_LOCATION line_or_no_assertion_or_none\n "
        "originator : PKG_ORIGINATOR actor_or_no_assertion\n supplier : PKG_SUPPLIER actor_or_no_assertion\n "
        "pkg_comment : PKG_COMMENT text_or_line\n "
        "pkg_copyright_text : PKG_COPYRIGHT_TEXT line_or_no_assertion_or_none\n "
        "pkg_license_declared : PKG_LICENSE_DECLARED license_or_no_assertion_or_none\n "
        "pkg_file_name : PKG_FILE_NAME LINE\n "
        "pkg_license_concluded : PKG_LICENSE_CONCLUDED license_or_no_assertion_or_none\n "
        "package_version : PKG_VERSION LINE\n pkg_license_comment : PKG_LICENSE_COMMENT text_or_line\n "
        "snippet_spdx_id : SNIPPET_SPDX_ID LINE\n snippet_name : SNIPPET_NAME LINE\n "
        "snippet_comment : SNIPPET_COMMENT text_or_line\n "
        "snippet_copyright_text : SNIPPET_COPYRIGHT_TEXT line_or_no_assertion_or_none\n "
        "snippet_license_comment : SNIPPET_LICENSE_COMMENT text_or_line\n "
        "file_spdx_id : SNIPPET_FILE_SPDXID LINE\n "
        "snippet_license_concluded : SNIPPET_LICENSE_CONCLUDED license_or_no_assertion_or_none\n "
        "annotation_spdx_id : ANNOTATION_SPDX_ID LINE\n "
        "annotation_comment : ANNOTATION_COMMENT text_or_line"
    )
    def p_generic_value(self, p):
        if p[1] in ELEMENT_EXPECTED_START_TAG.values():
            self.initialize_new_current_element(TAG_DATA_MODEL_FIELD[p[1]][0])
        if self.check_that_current_element_matches_class_for_value(TAG_DATA_MODEL_FIELD[p[1]][0], p.lineno(1)):
            set_value(p, self.current_element)

    @grammar_rule(
        "unknown_tag : UNKNOWN_TAG text_or_line\n | UNKNOWN_TAG ISO8601_DATE\n | UNKNOWN_TAG PERSON_VALUE \n"
        "| UNKNOWN_TAG"
    )
    def p_unknown_tag(self, p):
        self.logger.append(f"Unknown tag provided in line {p.lineno(1)}")

    @grammar_rule("text_or_line : TEXT\n line_or_no_assertion_or_none : TEXT")
    def p_text(self, p):
        p[0] = str_from_text(p[1])

    @grammar_rule(
        "text_or_line : LINE\n line_or_no_assertion : LINE\nline_or_no_assertion_or_none : LINE\n"
        "text_or_line : NO_ASSERTION\n text_or_line : NONE"
    )
    def p_line(self, p):
        p[0] = p[1]

    @grammar_rule(
        "license_or_no_assertion_or_none : NO_ASSERTION\n actor_or_no_assertion : NO_ASSERTION\n"
        "line_or_no_assertion : NO_ASSERTION\n line_or_no_assertion_or_none : NO_ASSERTION"
    )
    def p_no_assertion(self, p):
        p[0] = SpdxNoAssertion()

    @grammar_rule("license_or_no_assertion_or_none : NONE\n line_or_no_assertion_or_none : NONE")
    def p_none(self, p):
        p[0] = SpdxNone()

    @grammar_rule("license_or_no_assertion_or_none : LINE")
    def p_license(self, p):
        try:
            p[0] = get_spdx_licensing().parse(p[1])
        except ExpressionError as err:
            error_message = f"Error while parsing license expression: {p[1]}"
            if err.args:
                error_message += f": {err.args[0]}"
            self.current_element["logger"].append(error_message)

    @grammar_rule("actor_or_no_assertion : PERSON_VALUE\n | ORGANIZATION_VALUE")
    def p_actor_values(self, p):
        p[0] = ActorParser.parse_actor(p[1])

    @grammar_rule("spdx_id : SPDX_ID LINE")
    def p_spdx_id(self, p):
        # As all SPDX Ids share the same tag, there is no knowing which spdx_id belongs to the document.
        # We assume that to be the first spdx_id we encounter. As the specification does not explicitly require this,
        # our approach might lead to unwanted behavior when the document's SPDX Id is defined later in the document.
        if "spdx_id" in self.creation_info:
            self.current_element["spdx_id"] = p[2]
        else:
            self.creation_info["spdx_id"] = p[2]

    # parsing methods for creation info / document level

    @grammar_rule(
        "license_list_version : LICENSE_LIST_VERSION error\n document_comment : DOC_COMMENT error\n "
        "document_namespace : DOC_NAMESPACE error\n data_license : DOC_LICENSE error\n "
        "doc_name : DOC_NAME error\n ext_doc_ref : EXT_DOC_REF error\n spdx_version : DOC_VERSION error\n "
        "creator_comment : CREATOR_COMMENT error\n creator : CREATOR error\n created : CREATED error"
    )
    def p_creation_info_value_error(self, p):
        self.creation_info["logger"].append(
            f"Error while parsing {p[1]}: Token did not match specified grammar rule. Line: {p.lineno(1)}"
        )

    @grammar_rule(
        "document_comment : DOC_COMMENT text_or_line\n document_namespace : DOC_NAMESPACE LINE\n "
        "data_license : DOC_LICENSE LINE\n spdx_version : DOC_VERSION LINE\n "
        "creator_comment : CREATOR_COMMENT text_or_line\n doc_name : DOC_NAME LINE"
    )
    def p_generic_value_creation_info(self, p):
        set_value(p, self.creation_info)

    @grammar_rule("license_list_version : LICENSE_LIST_VERSION LINE")
    def p_license_list_version(self, p):
        set_value(p, self.creation_info, method_to_apply=Version.from_string)

    @grammar_rule("ext_doc_ref : EXT_DOC_REF LINE")
    def p_external_document_ref(self, p):
        external_doc_ref_regex = re.compile(r"(.*)(\s*SHA1:\s*[a-f0-9]{40})")
        external_doc_ref_match = external_doc_ref_regex.match(p[2])
        if not external_doc_ref_match:
            self.creation_info["logger"].append(
                f"Error while parsing ExternalDocumentRef: Couldn't match Checksum. Line: {p.lineno(1)}"
            )
            return
        try:
            document_ref_id, document_uri = external_doc_ref_match.group(1).strip().split(" ")
        except ValueError:
            self.creation_info["logger"].append(
                f"Error while parsing ExternalDocumentRef: Couldn't split the first part of the value into "
                f"document_ref_id and document_uri. Line: {p.lineno(1)}"
            )
            return
        checksum = parse_checksum(external_doc_ref_match.group(2).strip())
        external_document_ref = ExternalDocumentRef(document_ref_id, document_uri, checksum)
        self.creation_info.setdefault("external_document_refs", []).append(external_document_ref)

    @grammar_rule("creator : CREATOR PERSON_VALUE\n| CREATOR TOOL_VALUE\n| CREATOR ORGANIZATION_VALUE")
    def p_creator(self, p):
        self.creation_info.setdefault("creators", []).append(ActorParser.parse_actor(p[2]))

    @grammar_rule("created : CREATED ISO8601_DATE")
    def p_created(self, p):
        set_value(p, self.creation_info, method_to_apply=datetime_from_str)

    # parsing methods for extracted licensing info

    @grammar_rule("license_cross_ref : LICENSE_CROSS_REF LINE")
    def p_extracted_cross_reference(self, p):
        if self.check_that_current_element_matches_class_for_value(ExtractedLicensingInfo, p.lineno(1)):
            self.current_element.setdefault("cross_references", []).append(p[2])

    # parsing methods for file

    @grammar_rule("file_contributor : FILE_CONTRIBUTOR LINE")
    def p_file_contributor(self, p):
        if self.check_that_current_element_matches_class_for_value(File, p.lineno(1)):
            self.current_element.setdefault("contributors", []).append(p[2])

    @grammar_rule("file_attribution_text : FILE_ATTRIBUTION_TEXT text_or_line")
    def p_file_attribution_text(self, p):
        if self.check_that_current_element_matches_class_for_value(File, p.lineno(1)):
            self.current_element.setdefault("attribution_texts", []).append(p[2])

    @grammar_rule("file_license_info : FILE_LICENSE_INFO license_or_no_assertion_or_none")
    def p_file_license_info(self, p):
        if self.check_that_current_element_matches_class_for_value(File, p.lineno(1)):
            self.current_element.setdefault("license_info_in_file", []).append(p[2])

    @grammar_rule("file_type : FILE_TYPE LINE")
    def p_file_type(self, p):
        if not self.check_that_current_element_matches_class_for_value(File, p.lineno(1)):
            return
        try:
            file_type = FileType[p[2].strip()]
        except KeyError:
            self.current_element["logger"].append(f"Invalid FileType: {p[2]}. Line {p.lineno(1)}")
            return
        self.current_element.setdefault("file_types", []).append(file_type)

    @grammar_rule("file_checksum : FILE_CHECKSUM CHECKSUM")
    def p_file_checksum(self, p):
        if not self.check_that_current_element_matches_class_for_value(File, p.lineno(1)):
            return
        checksum = parse_checksum(p[2])
        self.current_element.setdefault("checksums", []).append(checksum)

    # parsing methods for package

    @grammar_rule("pkg_attribution_text : PKG_ATTRIBUTION_TEXT text_or_line")
    def p_pkg_attribution_text(self, p):
        self.check_that_current_element_matches_class_for_value(Package, p.lineno(1))
        self.current_element.setdefault("attribution_texts", []).append(p[2])

    @grammar_rule(
        "pkg_external_ref : PKG_EXTERNAL_REF LINE PKG_EXTERNAL_REF_COMMENT text_or_line\n | PKG_EXTERNAL_REF LINE"
    )
    def p_pkg_external_refs(self, p):
        if not self.check_that_current_element_matches_class_for_value(Package, p.lineno(1)):
            return
        try:
            category, reference_type, locator = p[2].split(" ")
        except ValueError:
            self.current_element["logger"].append(
                f"Couldn't split PackageExternalRef in category, reference_type and locator. Line: {p.lineno(1)}"
            )
            return
        comment = None
        if len(p) == 5:
            comment = p[4]
        try:
            category = ExternalPackageRefCategory[category.replace("-", "_")]
        except KeyError:
            self.current_element["logger"].append(
                f"Invalid ExternalPackageRefCategory: {category}. Line: {p.lineno(1)}"
            )
            return
        try:
            external_package_ref = construct_or_raise_parsing_error(
                ExternalPackageRef,
                {"category": category, "reference_type": reference_type, "locator": locator, "comment": comment},
            )
        except SPDXParsingError as err:
            self.current_element["logger"].append(err.get_messages())
            return
        self.current_element.setdefault("external_references", []).append(external_package_ref)

    @grammar_rule("pkg_license_info : PKG_LICENSE_INFO license_or_no_assertion_or_none")
    def p_pkg_license_info_from_file(self, p):
        if self.check_that_current_element_matches_class_for_value(Package, p.lineno(1)):
            self.current_element.setdefault("license_info_from_files", []).append(p[2])

    @grammar_rule("pkg_checksum : PKG_CHECKSUM CHECKSUM")
    def p_pkg_checksum(self, p):
        if not self.check_that_current_element_matches_class_for_value(Package, p.lineno(1)):
            return
        checksum = parse_checksum(p[2])
        self.current_element.setdefault("checksums", []).append(checksum)

    @grammar_rule("verification_code : PKG_VERIFICATION_CODE LINE")
    def p_pkg_verification_code(self, p):
        if not self.check_that_current_element_matches_class_for_value(Package, p.lineno(1)):
            return

        if "verification_code" in self.current_element:
            self.current_element["logger"].append(f"Multiple values for {p[1]} found. Line: {p.lineno(1)}")
            return
        verif_code_regex = re.compile(r"([0-9a-f]{40})\s*(\(excludes:\s*(.+)\))?", re.UNICODE)
        verif_code_code_grp = 1
        verif_code_exc_files_grp = 3
        match = verif_code_regex.match(p[2])
        if not match:
            self.current_element["logger"].append(
                f"Error while parsing {p[1]}: Value did not match expected format. Line: {p.lineno(1)}"
            )
            return
        value = match.group(verif_code_code_grp)
        excluded_files = None
        if match.group(verif_code_exc_files_grp):
            excluded_files = match.group(verif_code_exc_files_grp).split(",")
        self.current_element["verification_code"] = PackageVerificationCode(value, excluded_files)

    @grammar_rule("files_analyzed : PKG_FILES_ANALYZED LINE")
    def p_pkg_files_analyzed(self, p):
        if not self.check_that_current_element_matches_class_for_value(Package, p.lineno(1)):
            return
        if "files_analyzed" in self.current_element:
            self.current_element["logger"].append(f"Multiple values for {p[1]} found. Line: {p.lineno(1)}")
            return
        if p[2] == "true":
            self.current_element["files_analyzed"] = True
        elif p[2] == "false":
            self.current_element["files_analyzed"] = False
        else:
            self.current_element["logger"].append(
                f'The value of FilesAnalyzed must be either "true" or "false", but is: {p[2]}'
            )

    @grammar_rule("primary_package_purpose : PRIMARY_PACKAGE_PURPOSE LINE")
    def p_primary_package_purpose(self, p):
        if self.check_that_current_element_matches_class_for_value(Package, p.lineno(1)):
            set_value(p, self.current_element, method_to_apply=lambda x: PackagePurpose[x.replace("-", "_")])

    @grammar_rule(
        "built_date : BUILT_DATE ISO8601_DATE\n release_date : RELEASE_DATE ISO8601_DATE\n "
        "valid_until_date : VALID_UNTIL_DATE ISO8601_DATE"
    )
    def p_package_dates(self, p):
        if self.check_that_current_element_matches_class_for_value(Package, p.lineno(1)):
            set_value(p, self.current_element, method_to_apply=datetime_from_str)

    # parsing methods for snippet

    @grammar_rule("snippet_attribution_text : SNIPPET_ATTRIBUTION_TEXT text_or_line")
    def p_snippet_attribution_text(self, p):
        if self.check_that_current_element_matches_class_for_value(Snippet, p.lineno(1)):
            self.current_element.setdefault("attribution_texts", []).append(p[2])

    @grammar_rule("snippet_license_info : SNIPPET_LICENSE_INFO license_or_no_assertion_or_none")
    def p_snippet_license_info(self, p):
        if self.check_that_current_element_matches_class_for_value(Snippet, p.lineno(1)):
            self.current_element.setdefault("license_info_in_snippet", []).append(p[2])

    @grammar_rule("snippet_byte_range : SNIPPET_BYTE_RANGE LINE\n snippet_line_range : SNIPPET_LINE_RANGE LINE")
    def p_snippet_range(self, p):
        if not self.check_that_current_element_matches_class_for_value(Snippet, p.lineno(1)):
            return

        argument_name = TAG_DATA_MODEL_FIELD[p[1]][1]
        if argument_name in self.current_element:
            self.current_element["logger"].append(f"Multiple values for {p[1]} found. Line: {p.lineno(1)}")
            return
        range_re = re.compile(r"^(\d+):(\d+)$", re.UNICODE)
        if not range_re.match(p[2].strip()):
            self.current_element["logger"].append(
                f"Value for {p[1]} doesn't match valid range pattern. " f"Line: {p.lineno(1)}"
            )
            return
        startpoint = int(p[2].split(":")[0])
        endpoint = int(p[2].split(":")[-1])
        self.current_element[argument_name] = startpoint, endpoint

    # parsing methods for annotation

    @grammar_rule("annotator : ANNOTATOR PERSON_VALUE\n| ANNOTATOR TOOL_VALUE\n| ANNOTATOR ORGANIZATION_VALUE")
    def p_annotator(self, p):
        self.initialize_new_current_element(Annotation)
        set_value(p, self.current_element, method_to_apply=ActorParser.parse_actor)

    @grammar_rule("annotation_date : ANNOTATION_DATE ISO8601_DATE")
    def p_annotation_date(self, p):
        if self.check_that_current_element_matches_class_for_value(Annotation, p.lineno(1)):
            set_value(p, self.current_element, method_to_apply=datetime_from_str)

    @grammar_rule("annotation_type : ANNOTATION_TYPE LINE")
    def p_annotation_type(self, p):
        if self.check_that_current_element_matches_class_for_value(Annotation, p.lineno(1)):
            set_value(p, self.current_element, method_to_apply=lambda x: AnnotationType[x])

    # parsing methods for relationship

    @grammar_rule("relationship : RELATIONSHIP LINE RELATIONSHIP_COMMENT text_or_line\n " "| RELATIONSHIP LINE")
    def p_relationship(self, p):
        self.initialize_new_current_element(Relationship)
        try:
            spdx_element_id, relationship_type, related_spdx_element_id = p[2].split(" ")
        except ValueError:
            self.current_element["logger"].append(
                f"Relationship couldn't be split in spdx_element_id, relationship_type and "
                f"related_spdx_element. Line: {p.lineno(1)}"
            )
            return
        try:
            self.current_element["relationship_type"] = RelationshipType[relationship_type]
        except KeyError:
            self.current_element["logger"].append(f"Invalid RelationshipType {relationship_type}. Line: {p.lineno(1)}")
        if related_spdx_element_id == "NONE":
            related_spdx_element_id = SpdxNone()
        if related_spdx_element_id == "NOASSERTION":
            related_spdx_element_id = SpdxNoAssertion()
        self.current_element["related_spdx_element_id"] = related_spdx_element_id
        self.current_element["spdx_element_id"] = spdx_element_id
        if len(p) == 5:
            self.current_element["comment"] = p[4]

    def p_error(self, p):
        pass

    def parse(self, text):
        # entry point for the tag-value parser
        self.yacc.parse(text, lexer=self.lex)
        # this constructs the last remaining element; all other elements are constructed at the start of
        # their subsequent element
        self.construct_current_element()

        # To be able to parse creation info values if they appear in between other elements, e.g. packages, we use
        # two different dictionaries to collect the creation info and all other elements. Therefore, we have a separate
        # logger for the creation info whose messages we need to add to the main logger to than raise all collected
        # messages at once.
        creation_info_logger = self.creation_info.pop("logger")
        if creation_info_logger.has_messages():
            self.logger.extend([f"Error while parsing CreationInfo: {creation_info_logger.get_messages()}"])

        raise_parsing_error_if_logger_has_messages(self.logger)
        creation_info = construct_or_raise_parsing_error(CreationInfo, self.creation_info)
        self.elements_built["creation_info"] = creation_info
        document = construct_or_raise_parsing_error(Document, self.elements_built)
        return document

    def initialize_new_current_element(self, clazz: Any):
        self.construct_current_element()
        self.current_element["class"] = clazz

    def check_that_current_element_matches_class_for_value(self, expected_class, line_number) -> bool:
        if "class" not in self.current_element or expected_class != self.current_element["class"]:
            self.logger.append(
                f"Element {expected_class.__name__} is not the current element in scope, probably the expected tag to "
                f"start the element ({ELEMENT_EXPECTED_START_TAG[expected_class.__name__]}) is missing. "
                f"Line: {line_number}"
            )
            return False
        return True

    def construct_current_element(self):
        if "class" not in self.current_element:
            # This happens when the first element is initialized via initialize_new_current_element() or if the first
            # element is missing its expected starting tag. In both cases we are unable to construct an element.
            return

        clazz = self.current_element.pop("class")
        try:
            raise_parsing_error_if_logger_has_messages(self.current_element.pop("logger"), clazz.__name__)
            self.elements_built.setdefault(CLASS_MAPPING[clazz.__name__], []).append(
                construct_or_raise_parsing_error(clazz, self.current_element)
            )
            if clazz == File:
                self.check_for_preceding_package_and_build_contains_relationship()
        except SPDXParsingError as err:
            self.logger.extend(err.get_messages())
        self.current_element = {"logger": Logger()}

    def check_for_preceding_package_and_build_contains_relationship(self):
        file_spdx_id = self.current_element["spdx_id"]
        if "packages" not in self.elements_built:
            return
        # We assume that all files that are not contained in a package precede any package information. Any file
        # information that follows any package information is assigned to the last parsed package by creating a
        # corresponding contains relationship.
        # (see https://spdx.github.io/spdx-spec/v2.3/composition-of-an-SPDX-document/#5.2.2)
        if not self.elements_built["packages"]:
            self.logger.append(
                f"Error while building contains relationship for file {file_spdx_id}, "
                f"preceding package was not parsed successfully."
            )
            return
        package_spdx_id = self.elements_built["packages"][-1].spdx_id
        relationship = Relationship(package_spdx_id, RelationshipType.CONTAINS, file_spdx_id)
        if relationship not in self.elements_built.setdefault("relationships", []):
            self.elements_built["relationships"].append(relationship)
