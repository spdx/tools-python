# Copyright (c) 2014 Ahmed H. Ismail
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
from typing import Any, List, Dict

from license_expression import get_spdx_licensing
from ply import yacc
from ply.yacc import LRParser

from spdx.datetime_conversions import datetime_from_str
from spdx.model.annotation import AnnotationType, Annotation
from spdx.model.document import Document, CreationInfo
from spdx.model.external_document_ref import ExternalDocumentRef
from spdx.model.extracted_licensing_info import ExtractedLicensingInfo
from spdx.model.file import File, FileType
from spdx.model.package import Package, PackageVerificationCode, PackagePurpose, ExternalPackageRef, \
    ExternalPackageRefCategory
from spdx.model.relationship import Relationship, RelationshipType
from spdx.model.snippet import Snippet
from spdx.model.spdx_no_assertion import SpdxNoAssertion
from spdx.model.spdx_none import SpdxNone
from spdx.model.version import Version
from spdx.parser.actor_parser import ActorParser
from spdx.parser.error import SPDXParsingError
from spdx.parser.logger import Logger
from spdx.parser.parsing_functions import construct_or_raise_parsing_error, raise_parsing_error_if_logger_has_messages
from spdx.parser.tagvalue.lexer.tagvalue import SPDXLexer
from spdx.parser.tagvalue.parser.helper_methods import grammar_rule, str_from_text, parse_checksum, set_value

CLASS_MAPPING = dict(File="files", Annotation="annotations", Relationship="relationships", Snippet="snippets",
                     Package="packages", ExtractedLicensingInfo="extracted_licensing_info")
ELEMENT_EXPECTED_START_TAG = dict(File="FileName", Annotation="Annotator", Relationship="Relationship",
                                  Snippet="SnippetSPDXID", Package="PackageName", ExtractedLicensingInfo="LicenseID")


class Parser(object):
    tokens: List[str]
    logger: Logger
    current_element: Dict[str, Any]
    creation_info: Dict[str, Any]
    elements_build: Dict[str, Any]
    lex: SPDXLexer
    yacc: LRParser

    def __init__(self, **kwargs):
        self.tokens = SPDXLexer.tokens
        self.logger = Logger()
        self.current_element = {"logger": Logger()}
        self.creation_info = {"logger": Logger()}
        self.elements_build = dict()
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
        "| file_name\n| file_type\n| file_checksum\n| file_conc\n| file_lics_info\n| file_cr_text\n"
        "| file_lics_comment\n| file_attribution_text\n| file_notice\n| file_comment\n| file_contrib\n"
        # attributes for annotation
        "| annotator\n| annotation_date\n| annotation_comment\n| annotation_type\n| annotation_spdx_id\n"
        # attributes for relationship
        "| relationship\n"
        # attributes for snippet
        "| snip_spdx_id\n| snip_name\n| snip_comment\n| snippet_attribution_text\n| snip_cr_text\n"
        "| snip_lic_comment\n| file_spdx_id\n| snip_lics_conc\n| snip_lics_info\n| snip_byte_range\n"
        "| snip_line_range\n"
        # attributes for package
        "| package_name\n| package_version\n| download_location\n| files_analyzed\n| homepage\n"
        "| summary\n| source_info\n| pkg_file_name\n| supplier\n| originator\n| pkg_checksum\n"
        "| verification_code\n| description\n| pkg_comment\n| pkg_attribution_text\n| pkg_lic_decl\n| pkg_lic_conc\n"
        "| pkg_lic_ff\n| pkg_lic_comment\n| pkg_cr_text\n| pkg_ext_ref\n| primary_package_purpose\n"
        "| built_date\n| release_date\n| valid_until_date\n"
        # attributes for extracted licensing info
        "| license_id\n| extracted_text\n| license_name\n| lic_xref\n| lic_comment\n"
        "| unknown_tag ")
    def p_attrib(self, p):
        pass

    # general parsing methods
    @grammar_rule("unknown_tag : UNKNOWN_TAG text_or_line\n | UNKNOWN_TAG DATE\n | UNKNOWN_TAG PERSON_VALUE \n"
                  "| UNKNOWN_TAG")
    def p_unknown_tag(self, p):
        self.logger.append(f"Unknown tag provided in line {p.lineno(1)}")

    @grammar_rule("text_or_line : TEXT")
    def p_text(self, p):
        p[0] = str_from_text(p[1])

    @grammar_rule("text_or_line : LINE\n line_or_no_assertion : LINE\nline_or_no_assertion_or_none : text_or_line")
    def p_line(self, p):
        p[0] = p[1]

    @grammar_rule("license_or_no_assertion_or_none : NO_ASSERTION\n actor_or_no_assertion : NO_ASSERTION\n"
                  "line_or_no_assertion : NO_ASSERTION\n line_or_no_assertion_or_none : NO_ASSERTION")
    def p_no_assertion(self, p):
        p[0] = SpdxNoAssertion()

    @grammar_rule("license_or_no_assertion_or_none : NONE\n line_or_no_assertion_or_none : NONE")
    def p_none(self, p):
        p[0] = SpdxNone()

    @grammar_rule("license_or_no_assertion_or_none : LINE")
    def p_license(self, p):
        p[0] = get_spdx_licensing().parse(p[1])

    @grammar_rule("actor_or_no_assertion : PERSON_VALUE\n | ORG_VALUE")
    def p_actor_values(self, p):
        p[0] = ActorParser.parse_actor(p[1])

    @grammar_rule("spdx_id : SPDX_ID LINE")
    def p_spdx_id(self, p):
        # We assume that the documents spdx_id is defined first in the SPDXDocument, before any package or file
        # information. If this is not the case the parser will behave unexpectedly as the spdx_ids are assigned falsy.
        if "spdx_id" in self.creation_info:
            self.current_element["spdx_id"] = p[2]
        else:
            self.creation_info["spdx_id"] = p[2]

    # parsing methods for creation info / document level

    @grammar_rule("license_list_version : LIC_LIST_VER error\n document_comment : DOC_COMMENT error\n "
                  "document_namespace : DOC_NAMESPACE error\n data_license : DOC_LICENSE error\n "
                  "doc_name : DOC_NAME error\n ext_doc_ref : EXT_DOC_REF error\n spdx_version : DOC_VERSION error\n "
                  "creator_comment : CREATOR_COMMENT error\n creator : CREATOR error\n created : CREATED error")
    def p_creation_info_value_error(self, p):
        self.creation_info["logger"].append(
            f"Error while parsing {p[1]}: Token did not match specified grammar rule. Line: {p.lineno(1)}")

    @grammar_rule("document_comment : DOC_COMMENT text_or_line\n document_namespace : DOC_NAMESPACE LINE\n "
                  "data_license : DOC_LICENSE LINE\n spdx_version : DOC_VERSION LINE\n "
                  "creator_comment : CREATOR_COMMENT text_or_line")
    def p_generic_value_creation_info(self, p):
        set_value(p, self.creation_info)

    @grammar_rule("license_list_version : LIC_LIST_VER LINE")
    def p_license_list_version(self, p):
        set_value(p, self.creation_info, method_to_apply=Version.from_string)

    @grammar_rule("doc_name : DOC_NAME LINE")
    def p_doc_name(self, p):
        set_value(p, self.creation_info, argument_name="name")

    @grammar_rule("ext_doc_ref : EXT_DOC_REF DOC_REF_ID DOC_URI EXT_DOC_REF_CHECKSUM")
    def p_external_document_ref(self, p):
        document_ref_id = p[2]
        document_uri = p[3]
        checksum = parse_checksum(self.creation_info["logger"], p[4], p.lineno(1))
        external_document_ref = ExternalDocumentRef(document_ref_id, document_uri, checksum)
        self.creation_info.setdefault("external_document_refs", []).append(external_document_ref)

    def p_creator(self, p):
        """creator : CREATOR PERSON_VALUE\n| CREATOR TOOL_VALUE\n| CREATOR ORG_VALUE"""
        self.creation_info.setdefault("creators", []).append(ActorParser.parse_actor(p[2]))

    @grammar_rule("created : CREATED DATE")
    def p_created(self, p):
        set_value(p, self.creation_info, method_to_apply=datetime_from_str)

    # parsing methods for extracted licensing info

    @grammar_rule("license_id : LICS_ID error\n lic_xref : LICS_CRS_REF error\n lic_comment : LICS_COMMENT error\n "
                  "license_name : LICS_NAME error\n extracted_text : LICS_TEXT error")
    def p_extracted_licensing_info_value_error(self, p):
        self.current_element["logger"].append(
            f"Error while parsing {p[1]}: Token did not match specified grammar rule. Line: {p.lineno(1)}")

    @grammar_rule("license_name : LICS_NAME line_or_no_assertion\n extracted_text : LICS_TEXT text_or_line")
    def p_generic_value_extracted_licensing_info(self, p):
        self.check_that_current_element_matches_class_for_value(ExtractedLicensingInfo, p.lineno(1))
        set_value(p, self.current_element)

    @grammar_rule("license_id : LICS_ID LINE")
    def p_extracted_license_id(self, p):
        self.initialize_new_current_element(ExtractedLicensingInfo)
        set_value(p, self.current_element)

    @grammar_rule("lic_xref : LICS_CRS_REF LINE")
    def p_extracted_cross_reference(self, p):
        self.check_that_current_element_matches_class_for_value(ExtractedLicensingInfo, p.lineno(1))
        self.current_element.setdefault("cross_references", []).append(p[2])

    @grammar_rule("lic_comment : LICS_COMMENT text_or_line")
    def p_license_comment(self, p):
        self.check_that_current_element_matches_class_for_value(ExtractedLicensingInfo, p.lineno(1))
        set_value(p, self.current_element, argument_name="comment")

    # parsing methods for file

    @grammar_rule("file_contrib : FILE_CONTRIB error\n file_notice : FILE_NOTICE error\n "
                  "file_cr_text : FILE_CR_TEXT error\n file_lics_comment : FILE_LICS_COMMENT error\n "
                  "file_attribution_text : FILE_ATTRIBUTION_TEXT error\n file_lics_info : FILE_LICS_INFO error\n "
                  "file_comment : FILE_COMMENT error\n file_checksum : FILE_CHECKSUM error\n "
                  "file_conc : FILE_LICS_CONC error\n file_type : FILE_TYPE error")
    def p_file_value_error(self, p):
        self.current_element["logger"].append(
            f"Error while parsing {p[1]}: Token did not match specified grammar rule. Line: {p.lineno(1)}")

    @grammar_rule("file_name : FILE_NAME LINE")
    def p_file_name(self, p):
        self.initialize_new_current_element(File)
        set_value(p, self.current_element, argument_name="name")

    @grammar_rule("file_name : FILE_NAME error")
    def p_file_name_error(self, p):
        self.initialize_new_current_element(File)
        self.current_element["logger"].append(
            f"Error while parsing {p[1]}: Token did not match specified grammar rule. Line: {p.lineno(1)}")

    @grammar_rule("file_contrib : FILE_CONTRIB LINE")
    def p_file_contributor(self, p):
        self.check_that_current_element_matches_class_for_value(File, p.lineno(1))
        self.current_element.setdefault("contributors", []).append(p[2])

    @grammar_rule("file_notice : FILE_NOTICE text_or_line")
    def p_file_notice(self, p):
        self.check_that_current_element_matches_class_for_value(File, p.lineno(1))
        set_value(p, self.current_element, argument_name="notice")

    @grammar_rule("file_cr_text : FILE_CR_TEXT line_or_no_assertion_or_none")
    def p_file_copyright_text(self, p):
        self.check_that_current_element_matches_class_for_value(File, p.lineno(1))
        set_value(p, self.current_element, argument_name="copyright_text")

    @grammar_rule("file_lics_comment : FILE_LICS_COMMENT text_or_line")
    def p_file_license_comment(self, p):
        self.check_that_current_element_matches_class_for_value(File, p.lineno(1))
        set_value(p, self.current_element, argument_name="license_comment")

    @grammar_rule("file_attribution_text : FILE_ATTRIBUTION_TEXT text_or_line")
    def p_file_attribution_text(self, p):
        self.check_that_current_element_matches_class_for_value(File, p.lineno(1))
        self.current_element.setdefault("attribution_texts", []).append(p[2])

    @grammar_rule("file_lics_info : FILE_LICS_INFO license_or_no_assertion_or_none")
    def p_file_license_info(self, p):
        self.check_that_current_element_matches_class_for_value(File, p.lineno(1))
        if p[2] == SpdxNone() or p[2] == SpdxNoAssertion():
            self.current_element["license_info_in_file"] = p[2]
            return
        self.current_element.setdefault("license_info_in_file", []).append(p[2])

    @grammar_rule("file_comment : FILE_COMMENT text_or_line")
    def p_file_comment(self, p):
        self.check_that_current_element_matches_class_for_value(File, p.lineno(1))
        set_value(p, self.current_element, argument_name="comment")

    @grammar_rule("file_type : FILE_TYPE file_type_value")
    def p_file_type(self, p):
        self.check_that_current_element_matches_class_for_value(File, p.lineno(1))
        self.current_element.setdefault("file_type", []).append(FileType[p[2]])

    @grammar_rule(
        "file_type_value : SOURCE\n| BINARY\n| ARCHIVE\n | APPLICATION\n | AUDIO\n | IMAGE\n | FILETYPE_TEXT\n| VIDEO\n"
        " | DOCUMENTATION\n| SPDX \n| OTHER ")
    def p_file_type_value(self, p):
        p[0] = p[1]

    @grammar_rule("file_checksum : FILE_CHECKSUM CHECKSUM")
    def p_file_checksum(self, p):
        self.check_that_current_element_matches_class_for_value(File, p.lineno(1))
        checksum = parse_checksum(self.current_element["logger"], p[2], p.lineno(1))
        self.current_element.setdefault("checksums", []).append(checksum)

    @grammar_rule("file_conc : FILE_LICS_CONC license_or_no_assertion_or_none")
    def p_file_license_concluded(self, p):
        self.check_that_current_element_matches_class_for_value(File, p.lineno(1))
        set_value(p, self.current_element, argument_name="license_concluded")

    # parsing methods for package

    @grammar_rule("pkg_attribution_text : PKG_ATTRIBUTION_TEXT error\n description : PKG_DESC error\n "
                  "pkg_comment : PKG_COMMENT error\n summary : PKG_SUM error\n pkg_cr_text : PKG_CPY_TEXT error\n "
                  "pkg_ext_ref : PKG_EXT_REF error\n pkg_lic_comment : PKG_LICS_COMMENT error\n "
                  "pkg_lic_decl : PKG_LICS_DECL error\n pkg_lic_ff : PKG_LICS_FFILE error \n "
                  "pkg_lic_conc : PKG_LICS_CONC error\n source_info : PKG_SRC_INFO error\n homepage : PKG_HOME error\n "
                  "pkg_checksum : PKG_CHECKSUM error\n verification_code : PKG_VERF_CODE error\n "
                  "download_location : PKG_DOWN error\n files_analyzed : PKG_FILES_ANALYZED error\n "
                  "originator : PKG_ORIG error\n supplier : PKG_SUPPL error\n pkg_file_name : PKG_FILE_NAME error\n "
                  "package_version : PKG_VERSION error\n primary_package_purpose : PRIMARY_PACKAGE_PURPOSE error\n "
                  "built_date : BUILT_DATE error\n release_date : RELEASE_DATE error\n "
                  "valid_until_date : VALID_UNTIL_DATE error")
    def p_package_value_error(self, p):
        self.current_element["logger"].append(
            f"Error while parsing {p[1]}: Token did not match specified grammar rule. Line: {p.lineno(1)}")

    @grammar_rule("description : PKG_DESC text_or_line\n summary : PKG_SUM text_or_line\n "
                  "source_info : PKG_SRC_INFO text_or_line\n homepage : PKG_HOME line_or_no_assertion_or_none\n "
                  "download_location : PKG_DOWN line_or_no_assertion_or_none\n "
                  "originator : PKG_ORIG actor_or_no_assertion\n supplier : PKG_SUPPL actor_or_no_assertion")
    def p_generic_package_value(self, p):
        self.check_that_current_element_matches_class_for_value(Package, p.lineno(1))
        set_value(p, self.current_element)

    @grammar_rule("package_name : PKG_NAME LINE")
    def p_package_name(self, p):
        self.initialize_new_current_element(Package)
        set_value(p, self.current_element, argument_name="name")

    @grammar_rule("package_name : PKG_NAME error")
    def p_package_name_error(self, p):
        self.initialize_new_current_element(Package)
        self.current_element["logger"].append(
            f"Error while parsing {p[1]}: Token did not match specified grammar rule. Line: {p.lineno(1)}")

    @grammar_rule("pkg_comment : PKG_COMMENT text_or_line")
    def p_pkg_comment(self, p):
        self.check_that_current_element_matches_class_for_value(Package, p.lineno(1))
        set_value(p, self.current_element, argument_name="comment")

    @grammar_rule("pkg_attribution_text : PKG_ATTRIBUTION_TEXT text_or_line")
    def p_pkg_attribution_text(self, p):
        self.check_that_current_element_matches_class_for_value(Package, p.lineno(1))
        self.current_element.setdefault("attribution_texts", []).append(p[2])

    @grammar_rule("pkg_cr_text : PKG_CPY_TEXT line_or_no_assertion_or_none")
    def p_pkg_copyright_text(self, p):
        self.check_that_current_element_matches_class_for_value(Package, p.lineno(1))
        set_value(p, self.current_element, argument_name="copyright_text")

    @grammar_rule("pkg_ext_ref : PKG_EXT_REF LINE PKG_EXT_REF_COMMENT text_or_line\n | PKG_EXT_REF LINE")
    def p_pkg_external_refs(self, p):
        self.check_that_current_element_matches_class_for_value(Package, p.lineno(1))
        try:
            category, reference_type, locator = p[2].split(" ")
        except ValueError:
            self.current_element["logger"].append(
                f"Couldn't split PackageExternalRef in category, reference_type and locator. Line: {p.lineno(1)}")
            return
        comment = None
        if len(p) == 5:
            comment = p[4]
        try:
            category = ExternalPackageRefCategory[category.replace("-", "_")]
        except KeyError:
            self.current_element["logger"].append(f"Invalid ExternalPackageRefCategory: {category}")
            return
        try:
            external_package_ref = construct_or_raise_parsing_error(ExternalPackageRef,
                                                                    {"category": category,
                                                                     "reference_type": reference_type,
                                                                     "locator": locator,
                                                                     "comment": comment})
        except SPDXParsingError as err:
            self.current_element["logger"].append(err.get_messages())
            return
        self.current_element.setdefault("external_references", []).append(external_package_ref)

    @grammar_rule("pkg_lic_comment : PKG_LICS_COMMENT text_or_line")
    def p_pkg_license_comment(self, p):
        self.check_that_current_element_matches_class_for_value(Package, p.lineno(1))
        set_value(p, self.current_element, argument_name="license_comment")

    @grammar_rule("pkg_lic_decl : PKG_LICS_DECL license_or_no_assertion_or_none")
    def p_pkg_license_declared(self, p):
        self.check_that_current_element_matches_class_for_value(Package, p.lineno(1))
        set_value(p, self.current_element, argument_name="license_declared")

    @grammar_rule("pkg_lic_ff : PKG_LICS_FFILE license_or_no_assertion_or_none")
    def p_pkg_license_info_from_file(self, p):
        self.check_that_current_element_matches_class_for_value(Package, p.lineno(1))
        if p[2] == SpdxNone() or p[2] == SpdxNoAssertion():
            self.current_element["license_info_from_files"] = p[2]
        else:
            self.current_element.setdefault("license_info_from_files", []).append(p[2])

    @grammar_rule("pkg_lic_conc : PKG_LICS_CONC license_or_no_assertion_or_none")
    def p_pkg_license_concluded(self, p):
        self.check_that_current_element_matches_class_for_value(Package, p.lineno(1))
        set_value(p, self.current_element, argument_name="license_concluded")

    @grammar_rule("pkg_checksum : PKG_CHECKSUM CHECKSUM")
    def p_pkg_checksum(self, p):
        self.check_that_current_element_matches_class_for_value(Package, p.lineno(1))
        checksum = parse_checksum(self.current_element["logger"], p[2], p.lineno(1))
        self.current_element.setdefault("checksums", []).append(checksum)

    @grammar_rule("verification_code : PKG_VERF_CODE LINE")
    def p_pkg_verification_code(self, p):
        self.check_that_current_element_matches_class_for_value(Package, p.lineno(1))
        if str(p.slice[0]) in self.current_element:
            self.current_element["logger"].append(f"Multiple values for {p[1]} found. Line: {p.lineno(1)}")
            return
        verif_code_regex = re.compile(r"([0-9a-f]{40})\s*(\(excludes:\s*(.+)\))?", re.UNICODE)
        verif_code_code_grp = 1
        verif_code_exc_files_grp = 3
        match = verif_code_regex.match(p[2])
        if not match:
            self.current_element["logger"].append(
                f"Error while parsing {p[1]}: Value did not match expected format. Line: {p.lineno(1)}")
            return
        value = match.group(verif_code_code_grp)
        excluded_files = None
        if match.group(verif_code_exc_files_grp):
            excluded_files = match.group(verif_code_exc_files_grp).split(",")
        self.current_element[str(p.slice[0])] = PackageVerificationCode(value, excluded_files)

    @grammar_rule("files_analyzed : PKG_FILES_ANALYZED LINE")
    def p_pkg_files_analyzed(self, p):
        self.check_that_current_element_matches_class_for_value(Package, p.lineno(1))
        if str(p.slice[0]) in self.current_element:
            self.current_element["logger"].append(f"Multiple values for {p[1]} found. Line: {p.lineno(1)}")
            return
        self.current_element[str(p.slice[0])] = p[2] in ['true', 'True']

    @grammar_rule("pkg_file_name : PKG_FILE_NAME LINE")
    def p_pkg_file_name(self, p):
        self.check_that_current_element_matches_class_for_value(Package, p.lineno(1))
        set_value(p, self.current_element, argument_name="file_name")

    @grammar_rule("package_version : PKG_VERSION LINE")
    def p_package_version(self, p):
        self.check_that_current_element_matches_class_for_value(Package, p.lineno(1))
        set_value(p, self.current_element, argument_name="version")

    @grammar_rule("primary_package_purpose : PRIMARY_PACKAGE_PURPOSE primary_package_purpose_value")
    def p_primary_package_purpose(self, p):
        self.check_that_current_element_matches_class_for_value(Package, p.lineno(1))
        set_value(p, self.current_element, method_to_apply=lambda x: PackagePurpose[x.replace("-", "_")])

    @grammar_rule("primary_package_purpose_value : APPLICATION\n | FRAMEWORK\n | LIBRARY\n | CONTAINER\n "
                  "| OPERATING_SYSTEM \n | DEVICE \n| FIRMWARE\n | SOURCE\n | ARCHIVE\n | FILE\n | INSTALL\n | OTHER")
    def p_primary_package_purpose_value(self, p):
        p[0] = p[1]

    @grammar_rule("built_date : BUILT_DATE DATE\n release_date : RELEASE_DATE DATE\n "
                  "valid_until_date : VALID_UNTIL_DATE DATE")
    def p_package_dates(self, p):
        self.check_that_current_element_matches_class_for_value(Package, p.lineno(1))
        set_value(p, self.current_element, method_to_apply=datetime_from_str)

    # parsing methods for snippet

    @grammar_rule("snip_name : SNIPPET_NAME error\n snip_comment : SNIPPET_COMMENT error\n "
                  "snippet_attribution_text : SNIPPET_ATTRIBUTION_TEXT error\n snip_cr_text : SNIPPET_CR_TEXT error\n "
                  "snip_lic_comment : SNIPPET_LICS_COMMENT error\n file_spdx_id : SNIPPET_FILE_SPDXID error\n "
                  "snip_lics_conc : SNIPPET_LICS_CONC error\n snip_lics_info : SNIPPET_LICS_INFO error\n "
                  "snip_byte_range : SNIPPET_BYTE_RANGE error\n snip_line_range : SNIPPET_LINE_RANGE error\n ")
    def p_snippet_value_error(self, p):
        self.current_element["logger"].append(
            f"Error while parsing {p[1]}: Token did not match specified grammar rule. Line: {p.lineno(1)}")

    @grammar_rule("snip_spdx_id : SNIPPET_SPDX_ID LINE")
    def p_snippet_spdx_id(self, p):
        self.initialize_new_current_element(Snippet)
        set_value(p, self.current_element, argument_name="spdx_id")

    @grammar_rule("snip_spdx_id : SNIPPET_SPDX_ID error")
    def p_snippet_spdx_id_error(self, p):
        self.initialize_new_current_element(Snippet)
        self.current_element["logger"].append(
            f"Error while parsing {p[1]}: Token did not match specified grammar rule. Line: {p.lineno(1)}")

    @grammar_rule("snip_name : SNIPPET_NAME LINE")
    def p_snippet_name(self, p):
        self.check_that_current_element_matches_class_for_value(Snippet, p.lineno(1))
        set_value(p, self.current_element, argument_name="name")

    @grammar_rule("snip_comment : SNIPPET_COMMENT text_or_line")
    def p_snippet_comment(self, p):
        self.check_that_current_element_matches_class_for_value(Snippet, p.lineno(1))
        set_value(p, self.current_element, argument_name="comment")

    @grammar_rule("snippet_attribution_text : SNIPPET_ATTRIBUTION_TEXT text_or_line")
    def p_snippet_attribution_text(self, p):
        self.check_that_current_element_matches_class_for_value(Snippet, p.lineno(1))
        self.current_element.setdefault("attribution_texts", []).append(p[2])

    @grammar_rule("snip_cr_text : SNIPPET_CR_TEXT line_or_no_assertion_or_none")
    def p_snippet_copyright_text(self, p):
        self.check_that_current_element_matches_class_for_value(Snippet, p.lineno(1))
        set_value(p, self.current_element, argument_name="copyright_text")

    @grammar_rule("snip_lic_comment : SNIPPET_LICS_COMMENT text_or_line")
    def p_snippet_license_comment(self, p):
        self.check_that_current_element_matches_class_for_value(Snippet, p.lineno(1))
        set_value(p, self.current_element, argument_name="license_comment")

    @grammar_rule("file_spdx_id : SNIPPET_FILE_SPDXID LINE")
    def p_snippet_from_file_spdxid(self, p):
        self.check_that_current_element_matches_class_for_value(Snippet, p.lineno(1))
        set_value(p, self.current_element)

    @grammar_rule("snip_lics_conc : SNIPPET_LICS_CONC license_or_no_assertion_or_none")
    def p_snippet_concluded_license(self, p):
        self.check_that_current_element_matches_class_for_value(Snippet, p.lineno(1))
        set_value(p, self.current_element, argument_name="license_concluded")

    @grammar_rule("snip_lics_info : SNIPPET_LICS_INFO license_or_no_assertion_or_none")
    def p_snippet_license_info(self, p):
        self.check_that_current_element_matches_class_for_value(Snippet, p.lineno(1))
        if p[2] == SpdxNone() or p[2] == SpdxNoAssertion():
            self.current_element["license_info_in_snippet"] = p[2]
        else:
            self.current_element.setdefault("license_info_in_snippet", []).append(p[2])

    @grammar_rule("snip_byte_range : SNIPPET_BYTE_RANGE LINE")
    def p_snippet_byte_range(self, p):
        self.check_that_current_element_matches_class_for_value(Snippet, p.lineno(1))
        if "byte_range" in self.current_element:
            self.current_element["logger"].append(
                f"Multiple values for {p[1]} found. Line: {p.lineno(1)}")
        range_re = re.compile(r"^(\d+):(\d+)$", re.UNICODE)
        if not range_re.match(p[2].strip()):
            self.current_element["logger"].append(f"Value for SnippetByteRange doesn't match valid range pattern. "
                                                  f"Line: {p.lineno(1)}")
            return
        startpoint = int(p[2].split(":")[0])
        endpoint = int(p[2].split(":")[-1])
        self.current_element["byte_range"] = startpoint, endpoint

    @grammar_rule("snip_line_range : SNIPPET_LINE_RANGE LINE")
    def p_snippet_line_range(self, p):
        self.check_that_current_element_matches_class_for_value(Snippet, p.lineno(1))
        if "line_range" in self.current_element:
            self.current_element["logger"].append(
                f"Multiple values for {p[1]} found. Line: {p.lineno(1)}")
            return
        range_re = re.compile(r"^(\d+):(\d+)$", re.UNICODE)
        if not range_re.match(p[2].strip()):
            self.current_element["logger"].append(f"Value for SnippetLineRange doesn't match valid range pattern. "
                                                  f"Line: {p.lineno(1)}")
            return
        startpoint = int(p[2].split(":")[0])
        endpoint = int(p[2].split(":")[1])
        self.current_element["line_range"] = startpoint, endpoint

    # parsing methods for annotation

    @grammar_rule("annotation_date : ANNOTATION_DATE error\n annotation_comment : ANNOTATION_COMMENT error\n "
                  "annotation_type : ANNOTATION_TYPE error\n annotation_spdx_id : ANNOTATION_SPDX_ID error")
    def p_annotation_value_error(self, p):
        self.current_element["logger"].append(
            f"Error while parsing {p[1]}: Token did not match specified grammar rule. Line: {p.lineno(1)}")

    def p_annotator(self, p):
        """annotator : ANNOTATOR PERSON_VALUE\n| TOOL_VALUE\n| ORG_VALUE"""
        self.initialize_new_current_element(Annotation)
        set_value(p, self.current_element, method_to_apply=ActorParser.parse_actor)

    @grammar_rule("annotator : ANNOTATOR error")
    def p_annotator_error(self, p):
        self.initialize_new_current_element(Annotation)
        self.current_element["logger"].append(
            f"Error while parsing {p[1]}: Token did not match specified grammar rule. Line: {p.lineno(1)}")

    @grammar_rule("annotation_date : ANNOTATION_DATE DATE")
    def p_annotation_date(self, p):
        self.check_that_current_element_matches_class_for_value(Annotation, p.lineno(1))
        set_value(p, self.current_element, method_to_apply=datetime_from_str)

    @grammar_rule("annotation_comment : ANNOTATION_COMMENT text_or_line")
    def p_annotation_comment(self, p):
        self.check_that_current_element_matches_class_for_value(Annotation, p.lineno(1))
        set_value(p, self.current_element)

    @grammar_rule("annotation_type : ANNOTATION_TYPE annotation_type_value")
    def p_annotation_type(self, p):
        self.check_that_current_element_matches_class_for_value(Annotation, p.lineno(1))
        set_value(p, self.current_element, method_to_apply=lambda x: AnnotationType[x])

    @grammar_rule("annotation_type_value : OTHER\n| REVIEW")
    def p_annotation_type_value(self, p):
        p[0] = p[1]

    @grammar_rule("annotation_spdx_id : ANNOTATION_SPDX_ID LINE")
    def p_annotation_spdx_id(self, p):
        set_value(p, self.current_element, argument_name="spdx_id")

    # parsing methods for relationship

    @grammar_rule("relationship : RELATIONSHIP relationship_value RELATIONSHIP_COMMENT text_or_line\n "
                  "| RELATIONSHIP relationship_value")
    def p_relationship(self, p):
        self.initialize_new_current_element(Relationship)
        try:
            spdx_element_id, relationship_type, related_spdx_element_id = p[2].split(" ")
        except ValueError:
            self.current_element["logger"].append(
                f"Relationship couldn't be split in spdx_element_id, relationship_type and "
                f"related_spdx_element. Line: {p.lineno(1)}")
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

    @grammar_rule("relationship : RELATIONSHIP error")
    def p_relationship_error(self, p):
        self.initialize_new_current_element(Relationship)
        self.current_element["logger"].append(
            f"Error while parsing {p[1]}: Token did not match specified grammar rule. Line: {p.lineno(1)}")

    @grammar_rule("relationship_value : DOC_REF_ID LINE")
    def p_relationship_value_with_doc_ref(self, p):

        p[0] = p[1] + ":" + p[2]

    @grammar_rule("relationship_value : LINE")
    def p_relationship_value_without_doc_ref(self, p):

        p[0] = p[1]

    def p_error(self, p):
        pass

    def parse(self, text):
        self.yacc.parse(text, lexer=self.lex)
        self.construct_current_element()
        try:
            raise_parsing_error_if_logger_has_messages(self.creation_info.pop("logger"), "CreationInfo")
        except SPDXParsingError as err:
            self.logger.extend(err.get_messages())
        raise_parsing_error_if_logger_has_messages(self.logger)
        creation_info = construct_or_raise_parsing_error(CreationInfo, self.creation_info)
        self.elements_build["creation_info"] = creation_info
        document = construct_or_raise_parsing_error(Document, self.elements_build)
        return document

    def initialize_new_current_element(self, class_name: Any):
        self.construct_current_element()
        self.current_element["class"] = class_name

    def check_that_current_element_matches_class_for_value(self, expected_class, line_number):
        if "class" not in self.current_element:
            self.logger.append(
                f"Element {expected_class.__name__} is not the current element in scope, probably the expected tag to "
                f"start the element ({ELEMENT_EXPECTED_START_TAG[expected_class.__name__]}) is missing. "
                f"Line: {line_number}")
        elif expected_class != self.current_element["class"]:
            self.logger.append(
                f"Element {expected_class.__name__} is not the current element in scope, probably the expected tag to "
                f"start the element ({ELEMENT_EXPECTED_START_TAG[expected_class.__name__]}) is missing. "
                f"Line: {line_number}")

    def construct_current_element(self):
        if "class" not in self.current_element:
            self.current_element = {"logger": Logger()}
            return
        class_name = self.current_element.pop("class")
        try:
            raise_parsing_error_if_logger_has_messages(self.current_element.pop("logger"), class_name.__name__)
        except SPDXParsingError as err:
            self.logger.extend(err.get_messages())
            self.current_element = {"logger": Logger()}
            return
        try:
            self.elements_build.setdefault(CLASS_MAPPING[class_name.__name__], []).append(
                construct_or_raise_parsing_error(class_name, self.current_element))
            if class_name == File:
                self.check_for_preceding_package_and_build_contains_relationship()
        except SPDXParsingError as err:
            self.logger.extend(err.get_messages())
        self.current_element = {"logger": Logger()}

    def check_for_preceding_package_and_build_contains_relationship(self):
        file_spdx_id = self.current_element["spdx_id"]
        if "packages" not in self.elements_build:
            return
        # We assume that all files that are not contained in a package precede any package information. Any file
        # information that follows any package information is assigned to the last parsed package by creating a
        # corresponding contains relationship.
        # (see https://spdx.github.io/spdx-spec/v2.3/composition-of-an-SPDX-document/#5.2.2)
        package_spdx_id = self.elements_build["packages"][-1].spdx_id
        relationship = Relationship(package_spdx_id, RelationshipType.CONTAINS, file_spdx_id)
        if relationship not in self.elements_build.setdefault("relationships", []):
            self.elements_build.setdefault("relationships", []).append(relationship)
