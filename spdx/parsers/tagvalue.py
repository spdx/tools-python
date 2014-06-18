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
from ply import yacc
from .. import document

ERROR_MESSAGES = {
    'TOOL_VALUE' : 'Invalid tool value {0} at line: {1}',
    'ORG_VALUE' : 'Invalid organization value {0} at line: {1}',
    'PERSON_VALUE' : 'Invalid person value {0} at line: {1}',
    'CREATED_VALUE_TYPE' : 'Created value must be date in ISO 8601 format, line: {0}',
    'MORE_THAN_ONE' : 'Only one {0} allowed, extra at line: {1}',
    'CREATOR_COMMENT_VALUE_TYPE' : 'CreatorComment value must be free form text between <text></text> tags, line:{0}',
    'DOC_LICENSE_VALUE' : 'Invalid DataLicense value \'{0}\', line:{1} must be CC0-1.0',
    'DOC_LICENSE_VALUE_TYPE' : 'DataLicense must be CC0-1.0, line: {0}',
    'DOC_VERSION_VALUE' : 'Invalid SPDXVersion \'{0}\' must be SPDX-M.N where M and N are numbers. Line: {1}',
    'DOC_VERSION_VALUE_TYPE' : 'Invalid SPDXVersion value, must be SPDX-M.N where M and N are numbers. Line: {0}',
    'DOC_COMMENT_VALUE_TYPE' : 'DocumentComment value must be free form text between <text></text> tags, line:{0}',
    'REVIEWER_VALUE_TYPE' : 'Invalid Reviewer value must be a Person, Organization or Tool. Line: {0}',
    'CREATOR_VALUE_TYPE' : 'Invalid Reviewer value must be a Person, Organization or Tool. Line: {0}',
    'REVIEW_DATE_VALUE_TYPE' : 'ReviewDate value must be date in ISO 8601 format, line: {0}',
    'REVIEW_COMMENT_VALUE_TYPE' : 'ReviewComment value must be free form text between <text></text> tags, line:{0}',
    'A_BEFORE_B' : '{0} Can not appear before {1}, line: {2}',
}

class Parser(object):

    def __init__(self, builder, logger):
        super(Parser, self).__init__()
        self.tokens = Lexer.tokens
        self.builder = builder
        self.logger = logger
        self.error = False

    def p_start(self, p):
        'start : start attrib '    
        pass

    def p_start(self, p):
        'start : attrib '
        pass

    def p_attrib(self, p):
        '''attrib : spdx_version
                  | data_lics
                  | doc_comment
                  | creator
                  | created
                  | creator_comment
                  | locs_list_ver
                  | reviewer
                  | review_date
                  | review_comment
                  | PKG_NAME
                  | PKG_VERSION
                  | PKG_DOWN
                  | PKG_SUM
                  | PKG_SRC_INFO
                  | PKG_FILE_NAME
                  | PKG_SUPPL
                  | PKG_ORIG
                  | PKG_CHKSUM
                  | PKG_VERF_CODE
                  | PKG_DESC
                  | PKG_LICS_DECL
                  | PKG_LICS_CONC
                  | PKG_LICS_FFILE
                  | PKG_LICS_COMMENT
                  | PKG_CPY_TEXT
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
        '''
        p[0] = p[1]


    def p_reviewer(self, p):
        '''reviewer : REVIEWER entity'''
        ok =  self.builder.add_creator(doc=self.document, creator=p[2])
        self.error |=  not ok 

    def p_reviewer_1(self, p):
        '''reviewer : REVIEWER error'''
        self.error = True
        msg = ERROR_MESSAGES['REVIEWER_VALUE_TYPE'].format(p.lineno(1))
        self.logger.log(msg)

    def p_review_date(self, p):
        '''review_date : REVIEW_DATE DATE'''
        try:
            self.builder.add_review_date(reviewed=p[2], doc=self.document)
        except CardinalityError, e:
            self.error = True
            msg = ERROR_MESSAGES['MORE_THAN_ONE'].format('ReviewDate', p.lineno(1))
            self.logger.log(msg)
        except OrderError, e:
            self.error = True
            msg = ERROR_MESSAGES['A_BEFORE_B'].format('ReviewDate', 'Reviewer', 
                p.lineno(1))
            self.logger.log(msg)

    def p_review_date_1(self, p):
        '''review_date : REVIEW_DATE error'''
        self.error = True
        msg = ERROR_MESSAGES['REVIEW_DATE_VALUE_TYPE'].format(p.lineno(1))
        self.logger.log(msg)

    def p_review_comment(self, p):
        '''review_comment : REVIEW_COMMENT TEXT'''
        try:
            self.builder.add_review_comment(comment=p[2], doc=self.document)
        except CardinalityError, e:
            self.error = True
            msg = ERROR_MESSAGES['MORE_THAN_ONE'].format('ReviewComment', p.lineno(1))
            self.logger.log(msg)
        except OrderError, e:
            self.error = True
            msg = ERROR_MESSAGES['A_BEFORE_B'].format('ReviewComment', 'Reviewer', 
                p.lineno(1))
            self.logger.log(msg)

    def p_review_comment_1(self, p):
        '''review_comment : REVIEW_COMMENT error'''
        self.error = True
        msg = ERROR_MESSAGES['REVIEW_COMMENT_VALUE_TYPE'].format(p.lineno(1))
        self.logger.log(msg)

    def p_lics_list_ver(self, p):
        '''locs_list_ver : LIC_LIST_VER LINE'''
        try:
            self.builder.set_lics_list_ver(doc=self.document, value=p[2])
        except ValueError, e:
            self.error = True
            msg = ERROR_MESSAGES['LIC_LIST_VER_VALUE'].format(p[2], p.lineno(2))
            self.logger.log(msg)
        except CardinalityError, e:
            self.error = True
            msg = msg = ERROR_MESSAGES['MORE_THAN_ONE'].format('LicenseListVersion', p.lineno(1))
            self.logger.log(msg)

    def p_lics_list_ver_1(self, p):
        '''locs_list_ver : LIC_LIST_VER error'''
        self.error = True
        msg = ERROR_MESSAGES['LIC_LIST_VER_VALUE_TYPE'].format(p.lineno(1))
        self.logger.log(msg)


    def p_doc_comment(self, p):
        '''doc_comment : DOC_COMMENT TEXT'''
        try:
            self.builder.set_doc_comment(doc=self.document, comment=p[2])
        except CardinalityError, e:
            self.error = True
            msg = ERROR_MESSAGES['MORE_THAN_ONE'].format('DocumentComment', p.lineno(1))
            self.logger.log(msg)        

    def p_doc_comment_1(self, p):
        '''doc_comment : DOC_COMMENT error'''    
        self.error = True
        msg = ERROR_MESSAGES['DOC_COMMENT_VALUE_TYPE'].format(p.lineno(1))
        self.logger.log(msg)

    def p_data_license(self, p):
        '''data_lics : DOC_LICENSE LINE'''
        try:
            self.builder.set_doc_data_lics(doc=self.document, lics=p[2])
        except ValueError, e:
            self.error = True
            msg = ERROR_MESSAGES['DOC_LICENSE_VALUE'].format(p[2], p.lineno(2))
            self.logger.log(msg)
        except CardinalityError, e:
            self.error = True
            msg = ERROR_MESSAGES['MORE_THAN_ONE'].format('DataLicense', p.lineno(1))
            self.logger.log(msg)

    def p_data_license_1(self, p):
        '''data_lics : DOC_LICENSE error'''
        self.error = True
        msg = ERROR_MESSAGES['DOC_LICENSE_VALUE_TYPE'].format(p.lineno(1))
        self.logger.log(msg)

    def p_spdx_version(self, p):
        '''spdx_version : DOC_VERSION LINE'''
        try:
            self.builder.set_doc_version(doc=self.document, version=p[2])
        except CardinalityError, e:
            self.error = True
            msg = ERROR_MESSAGES['MORE_THAN_ONE'].format('SPDXVersion', p.lineno(1))
            self.logger.log(msg)
        except ValueError, e:
            self.error = True
            msg = ERROR_MESSAGES['DOC_VERSION_VALUE'].format(p[2], p.lineno(1))
            self.logger.log(msg)
        except IncompatibleVersionError, e:
            self.error = True
            self.logger.log('SPDXVersion must be SPDX-1.2 found {0}.'.format(value))
            
    def p_spdx_version(self, p):
        '''spdx_version : DOC_VERSION error'''
        self.error = True
        msg = ERROR_MESSAGES['DOC_VERSION_VALUE_TYPE'].format(p.lineno(1))
        self.logger.log(msg)

    def p_creator_comment(self, p):
        '''creator_comment : CREATOR_COMMENT TEXT'''
        try:
            self.builder.set_creation_comment(doc=self.document, comment=p[2])
        except CardinalityError, e:
            self.error = True
            msg = ERROR_MESSAGES['MORE_THAN_ONE'].format('CreatorComment', p.lineno(1))
            self.logger.log(msg)

    def p_creator_comment_1(self, p):
        '''creator_comment : CREATOR_COMMENT error'''
        self.error = True
        msg = ERROR_MESSAGES['CREATOR_COMMENT_VALUE_TYPE'].format(p.lineno(1))
        self.logger.log(msg)

    def p_creator(self, p):
        '''creator : CREATOR entity'''
        ok =  self.builder.add_creator(doc=self.document, creator=p[2])
        self.error |=  not ok 

    def p_creator_1(self, p):
        '''creator : CREATOR error'''
        self.error = True
        msg = ERROR_MESSAGES['CREATOR_VALUE_TYPE'].format(p.lineno(1))
        self.logger.log(msg)

    def p_created(self, p):
        '''created : CREATED DATE'''
        try:
            self.builder.set_created_date(doc=self.document, date=p[2])
        except CardinalityError, e:
            self.error = True
            msg = ERROR_MESSAGES['MORE_THAN_ONE'].format('Created', p.lineno(1))
            self.logger.log(msg)

    def p_created_2(self, p):
        '''created : CREATED error'''
        self.error = True
        msg = ERROR_MESSAGES['CREATED_VALUE_TYPE'].format(p.lineno(1))
        self.logger.log(msg)

    def p_entity(self, p):
        '''entity : TOOL_VALUE
        '''
        try:
            p[0] = self.builder.build_tool(doc=self.document, entity=p[1])
        except ValueError, e: 
            msg = ERROR_MESSAGES['TOOL_VALUE'].format(p[1], p.lineno(1))
            self.logger.log(msg)
            self.error = True
            p[0] = None
        
    def p_entity_2(self, p):
        '''entity : ORG_VALUE
        '''
        try:
            p[0] = self.builder.build_org(doc=self.document, entity=p[1])
        except ValueError, e:
            msg = ERROR_MESSAGES['ORG_VALUE'].format(p[1], p.lineno(1))
            self.logger.log(msg)
            self.error = True
            p[0] = None
        
    
    def p_entity_3(self, p):
        '''entity : PERSON_VALUE
        '''
        try:
            p[0] = self.builder.build_person(doc=self.document, entity=p[1])
        except ValueError, e:
            msg = ERROR_MESSAGES['PERSON_VALUE'].format(p[1], p.lineno(1))
            self.logger.log(msg)
            self.error = True
            p[0] = None

    def build(self, **kwargs):
        self.lex = Lexer()
        self.lex.build(reflags=re.UNICODE)
        self.yacc = yacc.yacc(module=self, **kwargs)

    def parse(self, text):
        self.document = document.Document()
        self.error = False
        self.yacc.parse(text, lexer=self.lex)
        return self.document



