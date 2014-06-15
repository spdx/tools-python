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
from .. import version


class ReviewsParser(object):
    """Parser for Tag/Value format review information."""
    def __init__(self):
        super(ReviewsParser, self).__init__()
    
    def p_reviews_1(self, p):
        'reviews : review_info'
        p[0] = list(p[1])

    def p_reviews_2(self, p):
        'reviews : reviews review_info'
        p[0] = p[1].append(p[2])

    def p_review_info(self, p):
        'review_info : reviewer rev_date review_comment'
        p[0] = self.builder.review_info(reviewers=p[1], rev_date=p[2], 
            comment=p[3])

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



class CreationInfoParser(object):
    """Parser for tag/value format Creation Info."""
    def __init__(self):
        super(CreationInfoParser, self).__init__()

    def p_creation_info(self, p):
        '''creation_info : creators created creator_comment lic_list_ver
        '''
        p[0] = self.builder.creation_info(creators=p[1], created=p[2],
            comment=p[3], lic_list_ver=p[4])

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


class DocMeta(object):
    """Parser for Tag/Value format document information."""

    def __init__(self):
        super(DocMeta, self).__init__()

    def p_doc_1(self, p):
        'doc : spdx_ver data_lic doc_comment'
        p[0] = self.builder.doc(spdx_ver=p[1], data_lic=p[2], doc_comment=p[3])

    def p_doc_2(self, p):
        'doc : spdx_ver data_lic'
        p[0] = self.builder.doc(spdx_ver=p[1], data_lic=p[2], doc_comment=None)

    def p_data_lic_1(self, p):
        'data_lic : DOC_LICENSE LINE'
        p[0] = self.builder.data_lic(value=p[2], line=p.lineno(2), 
            column=p.lexpos(2))

    def p_data_lic_2(self, p):
        'data_lic : DOC_LICENSE error'
        pass

    def p_data_lic_3(self, p):
        'data_lic : error any_value'
        pass

    def p_doc_comment_1(self, p):
        'doc_comment : DOC_COMMENT TEXT'
        p[0] = self.builder.doc_comment(text=p[2], line=p.lineno(2), 
            column=p.lexpos(2))

    def p_doc_comment_2(self, p):
        'doc_comment : DOC_COMMENT error'
        pass

    def p_spdx_ver_1(self, p):
        'spdx_ver : DOC_VERSION LINE'
        p[0] = self.builder.doc_version(value=p[2], line=p.lineno(2), 
            column=p.lexpos(2))

    def p_spdx_ver_2(self, p):
        'spdx_ver : DOC_VERSION error'
        pass

    def p_spdx_ver_3(self, p):
        'spdx_ver : error any_value'
        pass


class Parser(ReviewsParser, CreationInfoParser, DocMeta):

    start = 'start'

    def __init__(self, builder, logger):
        super(Parser, self).__init__()
        self.tokens = Lexer.tokens
        self.builder = builder
        self.logger = logger

    def p_start_1(self, p):
        '''start : doc creation_info reviews'''
        pass        

    def p_start_2(self, p):
        '''start : doc creation_info'''
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

    # def p_package(self, p):
    #     pass

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
        self.yacc = yacc.yacc(module=self, **kwargs)

    def parse(self, text):
        self.yacc.parse(text, lexer=self.lex)