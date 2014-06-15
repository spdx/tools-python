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
import nose
from spdx.parsers.tagvalue import Parser
from spdx.parsers.lexers.tagvalue import Lexer

class TestLexer(object):
    def __init__(self):
        self.l = Lexer()
        self.l.build()

    def test_document(self):
        data = '''
        SPDXVersion: SPDX-1.1
        # Comment.
        DataLicense: CC0-1.0
        DocumentComment: <text>This is a sample spreadsheet</text>
        '''
        self.l.input(data)
        self.token_assert_helper(self.l.token(), 'DOC_VERSION', 'SPDXVersion', 2)
        self.token_assert_helper(self.l.token(), 'LINE', 'SPDX-1.1', 2)
        self.token_assert_helper(self.l.token(), 'DOC_LICENSE', 'DataLicense', 4)
        self.token_assert_helper(self.l.token(), 'LINE', 'CC0-1.0', 4)
        self.token_assert_helper(self.l.token(), 'DOC_COMMENT', 'DocumentComment', 5)
        self.token_assert_helper(self.l.token(), 'TEXT', 
            '<text>This is a sample spreadsheet</text>',5)

    def test_creation_info(self):
        data = '''
        ## Creation Information
        Creator: Person: Gary O'Neall
        Creator: Organization: Source Auditor Inc.
        Creator: Tool: SourceAuditor-V1.2
        Created: 2010-02-03T00:00:00Z
        CreatorComment: <text>This is an example of an SPDX spreadsheet format</text>
        '''
        self.l.input(data)
        self.token_assert_helper(self.l.token(), 'CREATOR', 'Creator', 3)
        self.token_assert_helper(self.l.token(), 'PERSON_VALUE', "Person: Gary O'Neall",
            3)
        self.token_assert_helper(self.l.token(), 'CREATOR', 'Creator', 4)
        self.token_assert_helper(self.l.token(), 'ORG_VALUE',
            'Organization: Source Auditor Inc.', 4)
        self.token_assert_helper(self.l.token(), 'CREATOR', 'Creator', 5)
        self.token_assert_helper(self.l.token(), 'TOOL_VALUE',
            'Tool: SourceAuditor-V1.2', 5)
        self.token_assert_helper(self.l.token(), 'CREATED', 'Created', 6)
        self.token_assert_helper(self.l.token(), 'DATE', 
           '2010-02-03T00:00:00Z', 6)

    def test_review_info(self):
        data = '''
        Reviewer: Person: Joe Reviewer
        ReviewDate: 2010-02-10T00:00:00Z
        ReviewComment: <text>This is just an example.  
        Some of the non-standard licenses look like they are actually 
        BSD 3 clause licenses</text>
        '''
        self.l.input(data)
        self.token_assert_helper(self.l.token(), 'REVIEWER', 'Reviewer', 2)
        self.token_assert_helper(self.l.token(), 'PERSON_VALUE', 
            "Person: Joe Reviewer", 2)
        self.token_assert_helper(self.l.token(), 'REVIEW_DATE', 'ReviewDate', 3)
        self.token_assert_helper(self.l.token(), 'DATE', 
            '2010-02-10T00:00:00Z', 3)
        self.token_assert_helper(self.l.token(), 'REVIEW_COMMENT', 
            'ReviewComment', 4)
        self.token_assert_helper(self.l.token(), 'TEXT', 
            '''<text>This is just an example.  
        Some of the non-standard licenses look like they are actually 
        BSD 3 clause licenses</text>''', 4)


    def test_pacakage(self):
        data = '''
        PackageChecksum: SHA1: 2fd4e1c67a2d28fced849ee1bb76e7391b93eb12
        PackageVerificationCode: 4e3211c67a2d28fced849ee1bb76e7391b93feba (SpdxTranslatorSpdx.rdf, SpdxTranslatorSpdx.txt)
        '''
        self.l.input(data)
        self.token_assert_helper(self.l.token(), 'PKG_CHKSUM', 
            'PackageChecksum', 2)
        self.token_assert_helper(self.l.token(), 'CHKSUM', 
            'SHA1: 2fd4e1c67a2d28fced849ee1bb76e7391b93eb12', 2)
        self.token_assert_helper(self.l.token(), 'PKG_VERF_CODE', 
            'PackageVerificationCode', 3)
        self.token_assert_helper(self.l.token(), 'LINE',
            '4e3211c67a2d28fced849ee1bb76e7391b93feba (SpdxTranslatorSpdx.rdf, SpdxTranslatorSpdx.txt)',
            3)

    def token_assert_helper(self, token, type, value, line):
        print token
        assert token.type == type
        assert token.value == value
        assert token.lineno == line


class TestParser(object):
    
    def __init__(self):
        self.p = Parser(None, None)
        self.p.build()

    def test_file(self):
        assert 1 == 1
