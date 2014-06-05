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

from ply import lex

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
     ':' : 'COLON',
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
     'NONE' : 'NONE',
    }

    tokens = ['COMMENT', 'TEXT', 'TOOL_VALUE',
    'ORG_VALUE', 'PERSON_VALUE', 'DATE', 'VALUE'] + list(reserved.values())

    t_TOOL_VALUE = r'Tool:.*'
    t_ORG_VALUE = r'Organization:.*'
    t_PERSON_VALUE = r'Person:.*'
    t_DATE = r'\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\dZ'

    def t_COMMENT(self, t):
        r'\#.*'
        pass

    def t_TEXT(self, t):
        r'<text>((\n|.)+)</text>'
        t.value = t.lexer.lexmatch.group(1)
        # Count new lines
        t.lexer.lineno += t.value.count(r'\n')
        return t

    def t_VALUE(self, t):
        r'.+'
        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)