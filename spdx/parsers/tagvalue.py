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
from ply import lex, yacc
from .. import version

class Lexer(object):
    reserved = {
    # Top level fields
     'SPDXVersion' : 'DOC_VERSION',
     'DataLicense' : 'DOC_LICENSE',
     'DocumentComment': 'DOC_COMMENT',
     # Creation info
     'Creator' : 'CREATOR',
     'Created' : 'CREATED',
     'CreatorComment' : 'CREATOR_COMMENT',
     'LicenseListVersion' : 'LIC_LIST_VER',
     # Review info
     'Reviewer' : 'REVIEWER',
     'ReviewDate' : 'REVIEW_DATE',
     'ReviewComment' : 'REVIEW_COMMENT',
     # Package Fields
     'PackageName': 'PKG_NAME',
     'PackageVersion': 'PKG_VERSION',
     'PackageDownloadLocation': 'PKG_DOWN',
     'PackageSummary': 'OKG_SUM',
     'PackageSourceInfo': 'PKG_SRC_INFO',
     'PackageFileName' : 'PKG_FILE_NAME',
     'PackageSupplier' : 'PKG_SUPPL',
     'PackageOriginator' : 'PKG_ORIG',
     'PackageChecksum' : 'PKG_CHKSUM',
     'PackageVerificationCode' : 'PKG_VERF_CODE',
     'PackageDescription' : 'PKG_DESC',
     'PackageLicenseDeclared' : 'PKG_LICS_DECL',
     'PackageLicenseConcluded' : 'PKG_LICS_CONC',
     'PackageLicenseInfoFromFiles' : 'PKG_LICS_FFILE',
     'PackageLicenseComments' : 'PKG_LICS_COMMENT',
     # Files
     'FileName' : 'FILE_NAME',
     'FileType' : 'FILE_TYPE',
     'FileChecksum' : 'FILE_CHKSUM',
     'LicenseConcluded' : 'FILE_LICS_CONC',
     'LicenseInfoInFile' : 'FILE_LICS_INFO',
     'FileCopyrightText' : 'FILE_CR_TEXT',
     'LicenseComments' : 'FILE_LICS_COMMENT', 
     'FileComment' : 'FILE_COMMENT',
     'ArtifactOfProjectName' : 'ART_PRJ_NAME',
     'ArtifactOfProjectHomePage' : 'ART_PRJ_HOME',
     'ArtifactOfProjectURI' : 'ART_PRJ_URI',
     # License
     'LicenseID' : 'LICS_ID',
     'ExtractedText' : 'LICS_TEXT',
     'LicenseName' : 'LICS_NAME',
     'LicenseCrossReference' : 'LICS_CRS_REG',
     'LicenseComment' : 'LICS_COMMENT',
     # Common 
     'NOASSERTION' : 'NO_ASSERT',
     'UNKNOWN' : 'UN_KNOWN',
     'NONE' : 'NONE'
    }

    tokens = ['COMMENT', 'TEXT', 'TOOL_VALUE', 'UNKNOWN_TAG',
        'ORG_VALUE', 'PERSON_VALUE',
         'DATE', 'LINE', 'CHKSUM'] + list(reserved.values())

    def t_CHKSUM(self, t):
        r':\s?SHA1:\s[a-f0-9]{40,40}'
        t.value = t.value[1:].strip()
        return t

    def t_TOOL_VALUE(self, t):
        r':\s?Tool:.+'
        t.value = t.value[1:].strip()
        return t

    def t_ORG_VALUE(self, t):
        r':\s?Organization:.+'
        t.value = t.value[1:].strip()
        return t

    def t_PERSON_VALUE(self, t):
        r':\sPerson:.+'
        t.value = t.value[1:].strip()
        return t

    def t_DATE(self, t):
        r':\s?\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\dZ'
        t.value = t.value[1:].strip()
        return t

    def t_TEXT(self, t):
        r':\s?<text>(.|\n)+</text>'
        t.lexer.lineno += t.value.count('\n')
        t.value = t.value[1:].strip()
        return t

    def t_COMMENT(self, t):
        r'\#.*'
        pass         

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_whitespace(self, t):
        r'(\s|\t)+'
        pass

    def t_KEYWORD(self, t):
        r'[a-zA-Z]+'
        t.type = self.reserved.get(t.value,'UNKNOWN_TAG')
        t.value = t.value.strip()
        return t

    def t_LINE(self, t):
       r':.+'
       t.value = t.value[1:].strip()
       return t

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)
        
    def token(self):
        return self.lexer.token()
    
    def input(self, data):
        self.lexer.input(data)


class Parser(object):
    def __init__(self, builder, logger):
        self.tokens = Lexer.tokens
        self.builder = builder
        self.logger = logger

    

    def p_reviews_1(self, p):
        'reviews : review_info'
        p[0] = list(p[1])

    def p_reviews_2(self, p):
        'reviews : reviews review_info'
        p[0] = p[1].append(p[2])

    def p_reviews_3(self, p):
        'reviews : empty'
        p[0] = None

    def p_review_info_1(self, p):
        'review_info : reviewer rev_date review_comment'
        p[0] = self.builder.review_info(reviewers=p[1], rev_date=p[2], 
            comment=p[3])

    def p_review_info_2(self, p):
        'review_info : empty'
        p[0] = None

    def p_reviewer_1(self, p):
        'reviewer : REVIEWER entity'
        p[0] = p[1]

    def p_reviewer_2(self, p):
        'reviewer : REVIEWER error'
        pass

    def p_rev_date_1(self, p):
        'rev_date : REVIEW_DATE DATE'
        p[0] = self.builder.rev_date(value=p[2], line=p.lineno(2),
            column=p.lexpos(2))

    def p_rev_date_2(self, p):
        'rev_date : REVIEW_DATE error'
        pass

    def p_rev_date_3(self, p):
        'rev_date : error any_value'
        pass

    def p_review_comment_1(self, p):
        'review_comment : REVIEW_COMMENT TEXT'
        p[0] = self.review_comment(text=p[2], line=p.lineno(2),
         column=p.lexpos(2))

    def p_review_comment_2(self, p):
        'review_comment : REVIEW_COMMENT error'
        pass

    def p_review_comment_3(self, p):
        'review_comment : empty'
        p[0] = None


    def p_creation_info(self, p):
        '''creation_info : creators created creator_comment lic_list_ver
        '''
        p[0] = self.builder.creation_info(creators=p[1], created=p[2],
            comment=p[3], lic_list_ver=p[4])

    def p_lic_list_ver_1(self, p):
        'lic_list_ver : LIC_LIST_VER LINE'
        p[0] = self.builder.lic_list_ver(value=p[2], line=p.lineno(2), 
            column=p.lexpos(2))

    def p_lic_list_ver_2(self, p):
        'lic_list_ver : LIC_LIST_VER error'
        pass

    def p_lic_list_ver_3(self, p):
        'lic_list_ver : empty'
        p[0] = None

    def p_creator_comment_1(self, p):
        'creator_comment : CREATOR_COMMENT TEXT'
        p[0] = self.builder.creation_comment(text=p[2], line=p.lineno(2),
            column=p.lexpos(2))

    def p_creator_comment_2(self, p):
        'creator_comment : CREATOR_COMMENT error'
        pass

    def p_creator_comment_3(self, p):
        'creator_comment : empty'
        p[0] = None

    def p_created_1(self, p):
        'created : CREATED DATE'
        p[0] = self.builder.created(date=p[2], line=p.lineno(2), 
            column=p.lexpos(2))

    def p_created_2(self, p):
        'created : CREATED error'
        pass

    def p_created_3(self, p):
        'created : error any_value'
        pass

    def p_creators_1(self, p):
        'creators : creator'
        p[0] = list(p[1])

    def p_creators_2(self, p):
        'creators : creators creator'
        p[0] = p[1].append(p[2])

    def p_creator_1(self, p):
        'creator : CREATOR entity'
        p[0] = p[1]

    def p_creator_2(self, p):
        'creator : CREATOR error'
        pass

    def p_entity(self, p):
        '''entity : tool
                  | org
                  | person
        '''
        p[0] = p[1]


    def p_tool_1(self, p):
        'tool : TOOL_VALUE'
        p[0] = self.build_tool(value=p[1], line=p.lineno(1), column=p.lexpos(1))

    def p_org(self, p):
        'org : ORG_VALUE'
        p[0] = self.build_org(value=p[1], line=p.lineno(1), column=p.lexpos(1))

    def p_person(self, p):
        'person : PERSON_VALUE'
        p[0] = self.build_person(value=p[1], line=p.lineno(1), column=p.lexpos(1))

    def p_empty(self, p):
        'empty :'
        p[0] = None

    def p_any_value(self, p):
        '''any_value : LINE
                     | DATE
                     | TEXT
                     | NO_ASSERT
                     | UN_KNOWN
                     | NONE
                     | TOOL_VALUE
                     | ORG_VALUE
                     | PERSON_VALUE
                     | CHKSUM
        '''
        p[0] = p[1]

    def build(self, **kwargs):
        self.lex = Lexer()
        self.lex.build(reflags=re.UNICODE)
        self.yacc = yacc.yacc(module=self, method='SLR', **kwargs)

    def parse(self, text):
        self.yacc.parse(text, lexer=self.lex)