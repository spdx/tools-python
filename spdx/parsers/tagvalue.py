# Copyright 2014 Ahmed H. Ismail

#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at

#        http://www.apache.org/licenses/LICENSE-2.0

#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
import re
from lexers.tagvalue import Lexer
from tagvaluebuilders import CardinalityError, OrderError, ValueError, IncompatibleVersionError
from ply import yacc
from .. import document
from .. import utils

ERROR_MESSAGES = {
    'TOOL_VALUE': 'Invalid tool value {0} at line: {1}',
    'ORG_VALUE': 'Invalid organization value {0} at line: {1}',
    'PERSON_VALUE': 'Invalid person value {0} at line: {1}',
    'CREATED_VALUE_TYPE': 'Created value must be date in ISO 8601 format, line: {0}',
    'MORE_THAN_ONE': 'Only one {0} allowed, extra at line: {1}',
    'CREATOR_COMMENT_VALUE_TYPE': 'CreatorComment value must be free form text between <text></text> tags, line:{0}',
    'DOC_LICENSE_VALUE': 'Invalid DataLicense value \'{0}\', line:{1} must be CC0-1.0',
    'DOC_LICENSE_VALUE_TYPE': 'DataLicense must be CC0-1.0, line: {0}',
    'DOC_VERSION_VALUE': 'Invalid SPDXVersion \'{0}\' must be SPDX-M.N where M and N are numbers. Line: {1}',
    'DOC_VERSION_VALUE_TYPE': 'Invalid SPDXVersion value, must be SPDX-M.N where M and N are numbers. Line: {0}',
    'DOC_COMMENT_VALUE_TYPE': 'DocumentComment value must be free form text between <text></text> tags, line:{0}',
    'REVIEWER_VALUE_TYPE': 'Invalid Reviewer value must be a Person, Organization or Tool. Line: {0}',
    'CREATOR_VALUE_TYPE': 'Invalid Reviewer value must be a Person, Organization or Tool. Line: {0}',
    'REVIEW_DATE_VALUE_TYPE': 'ReviewDate value must be date in ISO 8601 format, line: {0}',
    'REVIEW_COMMENT_VALUE_TYPE': 'ReviewComment value must be free form text between <text></text> tags, line:{0}',
    'A_BEFORE_B': '{0} Can not appear before {1}, line: {2}',
    'PACKAGE_NAME_VALUE': 'PackageName must be single line of text, line: {0}',
    'PKG_VERSION_VALUE': 'PackageVersion must be single line of text, line: {0}',
    'PKG_FILE_NAME_VALUE': 'PackageFileName must be single line of text, line: {0}',
    'PKG_SUPPL_VALUE': 'PackageSupplier must be Organization, Person or NOASSERTION, line: {0}',
    'PKG_ORIG_VALUE': 'PackageOriginator must be Organization, Person or NOASSERTION, line: {0}',
    'PKG_DOWN_VALUE': 'PackageDownloadLocation must be a url or NONE or NOASSERTION, line: {0}',
    'PKG_HOME_VALUE': 'PackageHomePage must be a url or NONE or NOASSERTION, line: {0}',
    'PKG_SRC_INFO_VALUE': 'PackageSourceInfo must be free form text, line: {0}',
    'PKG_CHKSUM_VALUE': 'PackageChecksum must be a single line of text, line: {0}',
    'PKG_LICS_CONC_VALUE': 'PackageLicenseConcluded must be , line: {0}',
    'PKG_LIC_FFILE_VALUE': 'PackageLicenseInfoFromFiles must be, line: {0}',
    'PKG_LICS_DECL_VALUE': 'PackageLicenseDeclared must be, line: {0}',
    'PKG_LICS_COMMENT_VALUE': 'PackageLicenseComments must be free form text, line: {0}',
    'PKG_SUM_VALUE': 'PackageSummary must be free form text, line: {0}',
    'PKG_DESC_VALUE': 'PackageDescription must be free form text, line: {0}'

}


class Parser(object):

    def __init__(self, builder, logger):
        super(Parser, self).__init__()
        self.tokens = Lexer.tokens
        self.builder = builder
        self.logger = logger
        self.error = False

    def p_start_1(self, p):
        'start : start attrib '
        pass

    def p_start_2(self, p):
        'start : attrib '
        pass

    def p_attrib(self, p):
        """attrib : spdx_version
                  | data_lics
                  | doc_comment
                  | creator
                  | created
                  | creator_comment
                  | locs_list_ver
                  | reviewer
                  | review_date
                  | review_comment
                  | package_name
                  | package_version
                  | pkg_down_location
                  | pkg_home
                  | pkg_summary
                  | pkg_src_info
                  | pkg_file_name
                  | pkg_supplier
                  | pkg_orig
                  | pkg_chksum
                  | pkg_verif
                  | pkg_desc
                  | pkg_lic_decl
                  | pkg_lic_conc
                  | pkg_lic_ff
                  | pkg_lic_comment
                  | pkg_cr_text
                  | FILE_NAME
                  | FILE_TYPE
                  | FILE_CHKSUM
                  | FILE_LICS_CONC
                  | FILE_LICS_INFO
                  | FILE_CR_TEXT
                  | FILE_LICS_COMMENT
                  | FILE_COMMENT
                  | ART_PRJ_NAME
                  | ART_PRJ_HOME
                  | ART_PRJ_URI
                  | LICS_ID
                  | LICS_TEXT
                  | LICS_NAME
                  | LICS_CRS_REG
                  | LICS_COMMENT
        """
        pass

    def more_than_one_error(self, tag, line):
        self.error = True
        msg = ERROR_MESSAGES['MORE_THAN_ONE'].format(tag, line)
        self.logger.log(msg)

    def order_error(self, first_tag, second_tag, line):
        """Reports an OrderError. Error message will say that
        first_tag came before second_tag.
        """
        self.error = True
        msg = ERROR_MESSAGES['A_BEFORE_B'].format(first_tag,
                                                  second_tag, line)
        self.logger.log(msg)

    def p_pkg_desc_1(self, p):
        """pkg_desc : PKG_DESC TEXT"""
        try:
            self.builder.set_pkg_desc(self.document, p[2])
        except CardinalityError:
            self.more_than_one_error('PackageDescription', p.lineno(1))
        except OrderError:
            self.order_error('PackageDescription', 'PackageFileName',
                             p.lineno(1))

    def p_pkg_desc_2(self, p):
        """pkg_desc : PKG_DESC error"""
        self.error = True
        msg = ERROR_MESSAGES['PKG_DESC_VALUE'].format(p.lineno(1))
        self.logger.log(msg)

    def p_pkg_summary_1(self, p):
        """pkg_summary : PKG_SUM TEXT"""
        try:
            self.builder.set_pkg_summary(self.document, p[2])
        except OrderError:
            self.order_error('PackageSummary', 'PackageFileName', p.lineno(1))
        except CardinalityError:
            self.more_than_one_error('PackageSummary', p.lineno(1))

    def p_pkg_summary_2(self, p):
        """pkg_summary : PKG_SUM error"""
        self.error = True
        msg = ERROR_MESSAGES['PKG_SUM_VALUE'].format(p.lineno(1))
        self.logger.log(msg)

    def p_pkg_cr_text_1(self, p):
        """pkg_cr_text : PKG_CPY_TEXT pkg_cr_text_value"""
        try:
            self.builder.set_pkg_cr_text(self.document, p[2])
        except OrderError:
            self.order_error('PackageCopyrightText', 'PackageFileName',
                             p.lineno(1))
        except CardinalityError:
            self.more_than_one_error('PackageCopyrightText', p.lineno(1))

    def p_pkg_cr_text_2(self, p):
        """pkg_cr_text : PKG_CPY_TEXT error"""
        self.error = True
        msg = ERROR_MESSAGES['PKG_CPY_TEXT_VALUE'].format(p.lineno(1))

    def p_pkg_cr_text_value_1(self, p):
        """pkg_cr_text_value : TEXT"""
        p[0] = p[1]

    def p_pkg_cr_text_value_2(self, p):
        """pkg_cr_text_value : NONE"""
        p[0] = None

    def p_pkg_cr_text_value_3(self, p):
        """pkg_cr_text_value : NO_ASSERT"""
        p[0] = utils.NoAssert()

    def p_pkg_lic_comment_1(self, p):
        """pkg_lic_comment : PKG_LICS_COMMENT TEXT"""
        try:
            self.builder.set_pkg_license_comment(self.document, p[2])
        except OrderError:
            self.order_error('PackageLicenseComments', 'PackageFileName',
                             p.lineno(1))
        except CardinalityError:
            self.more_than_one_error('PackageLicenseComments', p.lineno(1))

    def p_pkg_lic_comment_2(self, p):
        """pkg_lic_comment : PKG_LICS_COMMENT error"""
        self.error = True
        msg = ERROR_MESSAGES['PKG_LICS_COMMENT_VALUE'].format(p.lineno(1))
        self.logger.log(msg)

    def p_pkg_lic_decl_1(self, p):
        """pkg_lic_decl : PKG_LICS_DECL pkg_lic_decl_value"""
        try:
            self.builder.set_pkg_license_declared(self.document, p[2])
        except OrderError:
            self.order_error(
                'PackageLicenseDeclared', 'PackageName', p.lineno(1))
        except CardinalityError:
            self.more_than_one_error('PackageLicenseDeclared', p.lineno(1))
        except ValueError:
            self.error = True
            msg = ERROR_MESSAGES['PKG_LICS_DECL_VALUE'].format(p.lineno(1))
            self.logger.log(msg)

    def p_pkg_lic_decl_2(self, p):
        """pkg_lic_decl : PKG_LICS_DECL error"""
        self.error = True
        msg = ERROR_MESSAGES['PKG_LICS_DECL_VALUE'].format(p.lineno(1))
        self.logger.log(msg)

    def p_pkg_lic_devl_value(self, p):
        """pkg_lic_decl_value : pkg_lic_conc_value"""
        p[0] = p[1]

    def p_pkg_lic_ff_1(self, p):
        """pkg_lic_ff : PKG_LICS_FFILE pkg_lic_ff_value"""
        try:
            self.builder.set_pkg_license_from_file(self.document, p[2])
        except OrderError:
            self.order_error('PackageLicenseInfoFromFiles', 'PackageName',
                             p.lineno(1))
        except ValueError:
            self.error = True
            msg = ERROR_MESSAGES['PKG_LIC_FFILE_VALUE'].format(p.lineno(1))
            self.logger.log(msg)

    def p_pkg_lic_ff_value_1(self, p):
        """pkg_lic_ff_value : NONE"""
        p[0] = None

    def p_pkg_lic_ff_value_2(self, p):
        """pkg_lic_ff_value : NO_ASSERT"""
        p[0] = utils.NoAssert()

    def p_pkg_lic_ff_value_3(self, p):
        """pkg_lic_ff_value : LINE"""
        p[0] = p[1]

    def p_pkg_lic_ff_2(self, p):
        """pkg_lic_ff : PKG_LICS_FFILE error"""
        self.error = True
        msg = ERROR_MESSAGES['PKG_LIC_FFILE_VALUE'].format(p.lineno(1))
        self.logger.log(msg)

    def p_pkg_lic_conc_1(self, p):
        """pkg_lic_conc : PKG_LICS_CONC pkg_lic_conc_value"""
        try:
            self.builder.set_pkg_licenses_concluded(self.document, p[2])
        except CardinalityError:
            self.more_than_one_error('PackageLicenseConcluded', p.lineno(1))
        except OrderError:
            self.order_error('PackageLicenseConcluded', 'PackageFileName',
                             p.lineno(1))
        except ValueError:
            self.error = True
            msg = ERROR_MESSAGES['PKG_LICS_CONC_VALUE'].format(p.lineno(1))
            self.logger.log(msg)

    def p_pkg_lic_conc_2(self, p):
        """pkg_lic_conc : PKG_LICS_CONC error"""
        self.error = True
        msg = ERROR_MESSAGES['PKG_LICS_CONC_VALUE'].format(p.lineno(1))
        self.logger.log(msg)

    def p_pkg_lic_conc_value_1(self, p):
        """pkg_lic_conc_value : LINE"""
        p[0] = p[1]

    def p_pkg_lic_conc_value_2(self, p):
        """pkg_lic_conc_value : NO_ASSERT"""
        p[0] = utils.NoAssert()

    def p_pkg_lic_conc_value_3(self, p):
        """pkg_lic_conc_value : NONE"""
        p[0] = None

    def p_pkg_src_info_1(self, p):
        """pkg_src_info : PKG_SRC_INFO TEXT"""
        try:
            self.builder.set_pkg_source_info(self.document, p[2])
        except CardinalityError:
            self.more_than_one_error('PackageSourceInfo', p.lineno(1))
        except OrderError:
            self.order_error(
                'PackageSourceInfo', 'PackageFileName', p.lineno(1))

    def p_pkg_src_info_2(self, p):
        """pkg_src_info : PKG_SRC_INFO error"""
        self.error = True
        msg = ERROR_MESSAGES['PKG_SRC_INFO_VALUE'].format(p.lineno(1))
        self.logger.log(msg)

    def p_pkg_chksum_1(self, p):
        """pkg_chksum : PKG_CHKSUM CHKSUM"""
        try:
            self.builder.set_pkg_chk_sum(self.document, p[2])
        except OrderError:
            self.order_error('PackageChecksum', 'PackageFileName', p.lineno(1))
        except CardinalityError:
            self.more_than_one_error('PackageChecksum', p.lineno(1))

    def p_pkg_chksum_2(self, p):
        """pkg_chksum : PKG_CHKSUM error"""
        self.error = True
        msg = ERROR_MESSAGES['PKG_CHKSUM_VALUE'].format(p.lineno(1))
        self.logger.log(msg)

    def p_pkg_verif_1(self, p):
        """pkg_verif : PKG_VERF_CODE LINE"""
        try:
            self.builder.set_pkg_verif_code(self.document, p[2])
        except OrderError:
            self.order_error(
                'PackageVerificationCode', 'PackageName', p.lineno(1))
        except CardinalityError:
            self.more_than_one_error('PackageVerificationCode', p.lineno(1))

    def p_pkg_verif_2(self, p):
        """pkg_verif : PKG_VERF_CODE error"""
        self.error = True
        msg = ERROR_MESSAGES['PKG_VERF_CODE_VALUE'].format(p.lineno(1))
        self.logger.log(msg)

    def p_pkg_home_1(self, p):
        """pkg_home : PKG_HOME pkg_home_value"""
        try:
            self.builder.set_pkg_down_location(self.document, p[2])
        except OrderError:
            self.order_error('PackageHomePage', 'PackageName', p.lineno(1))
        except CardinalityError:
            self.more_than_one_error('PackageHomePage', p.lineno(1))

    def p_pkg_home_2(self, p):
        """pkg_home : PKG_HOME error"""
        self.error = True
        msg = ERROR_MESSAGES['PKG_HOME_VALUE']
        self.logger.log(msg)

    def p_pkg_home_value_1(self, p):
        """pkg_home_value : LINE"""
        p[0] = p[1]

    def p_pkg_home_value_2(self, p):
        """pkg_home_value : NONE"""
        p[0] = None

    def p_pkg_home_value_3(self, p):
        """pkg_home_value : NO_ASSERT"""
        p[0] = utils.NoAssert()

    def p_pkg_down_location_1(self, p):
        """pkg_down_location : PKG_DOWN pkg_down_value"""
        try:
            self.builder.set_pkg_down_location(self.document, p[2])
        except OrderError:
            self.order_error(
                'PackageDownloadLocation', 'PackageName', p.lineno(1))
        except CardinalityError:
            self.more_than_one_error('PackageDownloadLocation', p.lineno(1))

    def p_pkg_down_location_2(self, p):
        """pkg_down_location : PKG_DOWN error"""
        self.error = True
        msg = ERROR_MESSAGES['PKG_DOWN_VALUE'].format(p.lineno(1))
        self.logger.log(msg)

    def p_pkg_down_value_1(self, p):
        """pkg_down_value : LINE """
        p[0] = p[1]

    def p_pkg_down_value_2(self, p):
        """pkg_down_value : NONE"""
        p[0] = None

    def p_pkg_down_value_3(self, p):
        """pkg_down_value : NO_ASSERT"""
        p[0] = utils.NoAssert()

    def p_pkg_orig_1(self, p):
        """pkg_orig : PKG_ORIG pkg_supplier_values"""
        try:
            self.builder.set_pkg_originator(self.document, p[2])
        except OrderError:
            self.order_error('PackageOriginator', 'PackageName', line)
        except ValueError:
            self.error = True
            msg = ERROR_MESSAGES['PKG_ORIG_VALUE'].format(p.lineno(1))
            self.logger.log(msg)
        except CardinalityError:
            self.more_than_one_error('PackageOriginator', p.lineno(1))

    def p_pkg_orig_2(self, p):
        """pkg_orig : PKG_ORIG error"""
        self.error = True
        self.error = True
        msg = ERROR_MESSAGES['PKG_ORIG_VALUE'].format(p.lineno(1))
        self.logger.log(msg)

    def p_pkg_supplier_1(self, p):
        """pkg_supplier : PKG_SUPPL pkg_supplier_values"""
        try:
            self.builder.set_pkg_supplier(self.document, p[2])
        except OrderError:
            self.order_error('PackageSupplier', 'PackageName', p.lineno(1))
        except CardinalityError:
            self.more_than_one_error('PackageSupplier', p.lineno(1))
        except ValueError:
            self.error = True
            msg = ERROR_MESSAGES['PKG_SUPPL_VALUE'].format(p.lineno(1))
            self.logger.log(msg)

    def p_pkg_supplier_2(self, p):
        """pkg_supplier : PKG_SUPPL error"""
        self.error = True
        msg = ERROR_MESSAGES['PKG_SUPPL_VALUE'].format(p.lineno(1))
        self.logger.log(msg)

    def p_pkg_supplier_values_1(self, p):
        """pkg_supplier_values : NO_ASSERT"""
        p[0] = utils.NoAssert()

    def p_pkg_supplier_values_2(self, p):
        """pkg_supplier_values : entity"""
        p[0] = p[1]

    def p_pkg_file_name(self, p):
        """pkg_file_name : PKG_FILE_NAME LINE"""
        try:
            self.builder.set_pkg_file_name(self.document, p[2])
        except OrderError:
            self.order_error('PackageFileName', 'PackageName', p.lineno(1))
        except CardinalityError:
            self.more_than_one_error('PackageFileName', p.lineno(1))

    def p_pkg_file_name_1(self, p):
        """pkg_file_name : PKG_FILE_NAME error"""
        self.error = True
        msg = ERROR_MESSAGES['PKG_FILE_NAME_VALUE'].format(p.lineno(1))
        self.logger.log(msg)

    def p_package_version_1(self, p):
        """package_version : PKG_VERSION LINE"""
        try:
            self.builder.set_pkg_vers(self.document, p[2])
        except OrderError:
            self.order_error('PackageVersion', 'PackageName', p.lineno(1))
        except CardinalityError:
            self.more_than_one_error('PackageVersion', p.lineno(1))

    def p_package_version_2(self, p):
        """package_version : PKG_VERSION error"""
        self.error = True
        msg = ERROR_MESSAGES['PKG_VERSION_VALUE'].format(p.lineno(1))
        self.logger.log(msg)

    def p_package_name(self, p):
        """package_name : PKG_NAME LINE"""
        try:
            self.builder.create_package(self.document, p[2])
        except CardinalityError:
            self.more_than_one_error('PackageName', p.lineno(1))

    def p_package_name_1(self, p):
        """package_name : PKG_NAME error"""
        self.error = True
        msg = ERROR_MESSAGES['PACKAGE_NAME_VALUE'].format(p.lineno(1))
        self.logger.log(msg)

    def p_reviewer_1(self, p):
        """reviewer : REVIEWER entity"""
        self.builder.add_reviewer(self.document, p[2])

    def p_reviewer_2(self, p):
        """reviewer : REVIEWER error"""
        self.error = True
        msg = ERROR_MESSAGES['REVIEWER_VALUE_TYPE'].format(p.lineno(1))
        self.logger.log(msg)

    def p_review_date_1(self, p):
        """review_date : REVIEW_DATE DATE"""
        try:
            self.builder.add_review_date(self.document, p[2])
        except CardinalityError:
            self.more_than_one_error('ReviewDate', p.lineno(1))
        except OrderError:
            self.order_error('ReviewDate', 'Reviewer', p.lineno(1))

    def p_review_date_2(self, p):
        """review_date : REVIEW_DATE error"""
        self.error = True
        msg = ERROR_MESSAGES['REVIEW_DATE_VALUE_TYPE'].format(p.lineno(1))
        self.logger.log(msg)

    def p_review_comment_1(self, p):
        """review_comment : REVIEW_COMMENT TEXT"""
        try:
            self.builder.add_review_comment(self.document, p[2])
        except CardinalityError:
            self.more_than_one_error('ReviewComment', p.lineno(1))
        except OrderError:
            self.order_error('ReviewComment', 'Reviewer', p.lineno(1))

    def p_review_comment_2(self, p):
        """review_comment : REVIEW_COMMENT error"""
        self.error = True
        msg = ERROR_MESSAGES['REVIEW_COMMENT_VALUE_TYPE'].format(p.lineno(1))
        self.logger.log(msg)

    def p_lics_list_ver_1(self, p):
        """locs_list_ver : LIC_LIST_VER LINE"""
        try:
            self.builder.set_lics_list_ver(self.document, p[2])
        except ValueError:
            self.error = True
            msg = ERROR_MESSAGES['LIC_LIST_VER_VALUE'].format(
                p[2], p.lineno(2))
            self.logger.log(msg)
        except CardinalityError:
            self.more_than_one_error('LicenseListVersion', p.lineno(1))

    def p_lics_list_ver_2(self, p):
        """locs_list_ver : LIC_LIST_VER error"""
        self.error = True
        msg = ERROR_MESSAGES['LIC_LIST_VER_VALUE_TYPE'].format(p.lineno(1))
        self.logger.log(msg)

    def p_doc_comment_1(self, p):
        """doc_comment : DOC_COMMENT TEXT"""
        try:
            self.builder.set_doc_comment(self.document, p[2])
        except CardinalityError:
            self.more_than_one_error('DocumentComment', p.lineno(1))

    def p_doc_comment_2(self, p):
        """doc_comment : DOC_COMMENT error"""
        self.error = True
        msg = ERROR_MESSAGES['DOC_COMMENT_VALUE_TYPE'].format(p.lineno(1))
        self.logger.log(msg)

    def p_data_license_1(self, p):
        """data_lics : DOC_LICENSE LINE"""
        try:
            self.builder.set_doc_data_lics(self.document, p[2])
        except ValueError:
            self.error = True
            msg = ERROR_MESSAGES['DOC_LICENSE_VALUE'].format(p[2], p.lineno(2))
            self.logger.log(msg)
        except CardinalityError:
            self.more_than_one_error('DataLicense', p.lineno(1))

    def p_data_license_2(self, p):
        """data_lics : DOC_LICENSE error"""
        self.error = True
        msg = ERROR_MESSAGES['DOC_LICENSE_VALUE_TYPE'].format(p.lineno(1))
        self.logger.log(msg)

    def p_spdx_version_1(self, p):
        """spdx_version : DOC_VERSION LINE"""
        try:
            self.builder.set_doc_version(self.document, p[2])
        except CardinalityError:
            self.more_than_one_error('SPDXVersion', p.lineno(1))
        except ValueError:
            self.error = True
            msg = ERROR_MESSAGES['DOC_VERSION_VALUE'].format(p[2], p.lineno(1))
            self.logger.log(msg)
        except IncompatibleVersionError:
            self.error = True
            self.logger.log(
                'SPDXVersion must be SPDX-1.2 found {0}.'.format(value))

    def p_spdx_version_2(self, p):
        """spdx_version : DOC_VERSION error"""
        self.error = True
        msg = ERROR_MESSAGES['DOC_VERSION_VALUE_TYPE'].format(p.lineno(1))
        self.logger.log(msg)

    def p_creator_comment_1(self, p):
        """creator_comment : CREATOR_COMMENT TEXT"""
        try:
            self.builder.set_creation_comment(self.document, p[2])
        except CardinalityError:
            self.more_than_one_error('CreatorComment', p.lineno(1))

    def p_creator_comment_2(self, p):
        """creator_comment : CREATOR_COMMENT error"""
        self.error = True
        msg = ERROR_MESSAGES['CREATOR_COMMENT_VALUE_TYPE'].format(p.lineno(1))
        self.logger.log(msg)

    def p_creator_1(self, p):
        """creator : CREATOR entity"""
        self.builder.add_creator(self.document, p[2])

    def p_creator_2(self, p):
        """creator : CREATOR error"""
        self.error = True
        msg = ERROR_MESSAGES['CREATOR_VALUE_TYPE'].format(p.lineno(1))
        self.logger.log(msg)

    def p_created_1(self, p):
        """created : CREATED DATE"""
        try:
            self.builder.set_created_date(self.document, p[2])
        except CardinalityError:
            self.more_than_one_error('Created', p.lineno(1))

    def p_created_2(self, p):
        """created : CREATED error"""
        self.error = True
        msg = ERROR_MESSAGES['CREATED_VALUE_TYPE'].format(p.lineno(1))
        self.logger.log(msg)

    def p_entity_1(self, p):
        """entity : TOOL_VALUE
        """
        try:
            p[0] = self.builder.build_tool(self.document, p[1])
        except ValueError:
            msg = ERROR_MESSAGES['TOOL_VALUE'].format(p[1], p.lineno(1))
            self.logger.log(msg)
            self.error = True
            p[0] = None

    def p_entity_2(self, p):
        """entity : ORG_VALUE
        """
        try:
            p[0] = self.builder.build_org(self.document, p[1])
        except ValueError:
            msg = ERROR_MESSAGES['ORG_VALUE'].format(p[1], p.lineno(1))
            self.logger.log(msg)
            self.error = True
            p[0] = None

    def p_entity_3(self, p):
        """entity : PERSON_VALUE
        """
        try:
            p[0] = self.builder.build_person(self.document, p[1])
        except ValueError:
            msg = ERROR_MESSAGES['PERSON_VALUE'].format(p[1], p.lineno(1))
            self.logger.log(msg)
            self.error = True
            p[0] = None

    def p_error(self, p):
        print 'Parser error'

    def build(self, **kwargs):
        self.lex = Lexer()
        self.lex.build(reflags=re.UNICODE)
        self.yacc = yacc.yacc(module=self, **kwargs)

    def parse(self, text):
        self.document = document.Document()
        self.error = False
        self.yacc.parse(text, lexer=self.lex)
        return self.document, self.error
