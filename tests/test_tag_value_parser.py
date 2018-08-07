# Copyright (c) 2014 Ahmed H. Ismail
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import sys
import unittest
from unittest import TestCase

import spdx
from spdx.parsers.tagvalue import Parser
from spdx.parsers.lexers.tagvalue import Lexer
from spdx.parsers.tagvaluebuilders import Builder
from spdx.parsers.loggers import StandardLogger
from spdx.version import Version


class TestLexer(TestCase):

    def setUp(self):
        self.l = Lexer()
        self.l.build()

    def test_document(self):
        data = '''
        SPDXVersion: SPDX-2.1
        # Comment.
        DataLicense: CC0-1.0
        DocumentName: Sample_Document-V2.1
        SPDXID: SPDXRef-DOCUMENT
        DocumentNamespace: https://spdx.org/spdxdocs/spdx-example-444504E0-4F89-41D3-9A0C-0305E82C3301
        DocumentComment: <text>This is a sample spreadsheet</text>
        '''
        self.l.input(data)
        self.token_assert_helper(self.l.token(), 'DOC_VERSION', 'SPDXVersion', 2)
        self.token_assert_helper(self.l.token(), 'LINE', 'SPDX-2.1', 2)
        self.token_assert_helper(self.l.token(), 'DOC_LICENSE', 'DataLicense', 4)
        self.token_assert_helper(self.l.token(), 'LINE', 'CC0-1.0', 4)
        self.token_assert_helper(self.l.token(), 'DOC_NAME', 'DocumentName', 5)
        self.token_assert_helper(self.l.token(), 'LINE', 'Sample_Document-V2.1',
                                 5)
        self.token_assert_helper(self.l.token(), 'SPDX_ID', 'SPDXID', 6)
        self.token_assert_helper(self.l.token(), 'LINE', 'SPDXRef-DOCUMENT', 6)
        self.token_assert_helper(self.l.token(), 'DOC_NAMESPACE',
                                 'DocumentNamespace', 7)
        self.token_assert_helper(self.l.token(), 'LINE',
                                 'https://spdx.org/spdxdocs/spdx-example-444504E0-4F89-41D3-9A0C-0305E82C3301',
                                 7)
        self.token_assert_helper(self.l.token(), 'DOC_COMMENT', 'DocumentComment', 8)
        self.token_assert_helper(self.l.token(), 'TEXT', '<text>This is a sample spreadsheet</text>', 8)

    def test_external_document_references(self):
        data = '''
        ExternalDocumentRef:DocumentRef-spdx-tool-2.1 http://spdx.org/spdxdocs/spdx-tools-v2.1-3F2504E0-4F89-41D3-9A0C-0305E82C3301 SHA1: d6a770ba38583ed4bb4525bd96e50461655d2759
        '''
        self.l.input(data)
        self.token_assert_helper(self.l.token(), 'EXT_DOC_REF',
                                 'ExternalDocumentRef', 2)
        self.token_assert_helper(self.l.token(), 'DOC_REF_ID',
                                 'DocumentRef-spdx-tool-2.1', 2)
        self.token_assert_helper(self.l.token(), 'DOC_URI',
                                 'http://spdx.org/spdxdocs/spdx-tools-v2.1-3F25'
                                 '04E0-4F89-41D3-9A0C-0305E82C3301', 2)
        self.token_assert_helper(self.l.token(), 'EXT_DOC_REF_CHKSUM',
                                 'SHA1: '
                                 'd6a770ba38583ed4bb4525bd96e50461655d2759', 2)


    def test_creation_info(self):
        data = '''
        ## Creation Information
        Creator: Person: Gary O'Neall
        Creator: Organization: Source Auditor Inc.
        Creator: Tool: SourceAuditor-V1.2
        Created: 2010-02-03T00:00:00Z
        CreatorComment: <text>This is an example of an SPDX
        spreadsheet format</text>
        '''
        self.l.input(data)
        self.token_assert_helper(self.l.token(), 'CREATOR', 'Creator', 3)
        self.token_assert_helper(self.l.token(), 'PERSON_VALUE', "Person: Gary O'Neall", 3)
        self.token_assert_helper(self.l.token(), 'CREATOR', 'Creator', 4)
        self.token_assert_helper(self.l.token(), 'ORG_VALUE', 'Organization: Source Auditor Inc.', 4)
        self.token_assert_helper(self.l.token(), 'CREATOR', 'Creator', 5)
        self.token_assert_helper(self.l.token(), 'TOOL_VALUE', 'Tool: SourceAuditor-V1.2', 5)
        self.token_assert_helper(self.l.token(), 'CREATED', 'Created', 6)
        self.token_assert_helper(self.l.token(), 'DATE', '2010-02-03T00:00:00Z', 6)

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
        self.token_assert_helper(self.l.token(), 'PERSON_VALUE', "Person: Joe Reviewer", 2)
        self.token_assert_helper(self.l.token(), 'REVIEW_DATE', 'ReviewDate', 3)
        self.token_assert_helper(self.l.token(), 'DATE', '2010-02-10T00:00:00Z', 3)
        self.token_assert_helper(self.l.token(), 'REVIEW_COMMENT', 'ReviewComment', 4)
        self.token_assert_helper(self.l.token(), 'TEXT', '''<text>This is just an example.
        Some of the non-standard licenses look like they are actually
        BSD 3 clause licenses</text>''', 4)

    def test_pacakage(self):
        data = '''
        PackageChecksum: SHA1: 2fd4e1c67a2d28fced849ee1bb76e7391b93eb12
        PackageVerificationCode: 4e3211c67a2d28fced849ee1bb76e7391b93feba (SpdxTranslatorSpdx.rdf, SpdxTranslatorSpdx.txt)
        '''
        self.l.input(data)
        self.token_assert_helper(self.l.token(), 'PKG_CHKSUM', 'PackageChecksum', 2)
        self.token_assert_helper(self.l.token(), 'CHKSUM', 'SHA1: 2fd4e1c67a2d28fced849ee1bb76e7391b93eb12', 2)
        self.token_assert_helper(self.l.token(), 'PKG_VERF_CODE', 'PackageVerificationCode', 3)
        self.token_assert_helper(self.l.token(), 'LINE', '4e3211c67a2d28fced849ee1bb76e7391b93feba (SpdxTranslatorSpdx.rdf, SpdxTranslatorSpdx.txt)', 3)

    def test_unknown_tag(self):
        data = '''
        SomeUnknownTag: SomeUnknownValue
        '''
        self.l.input(data)
        self.token_assert_helper(self.l.token(), 'UNKNOWN_TAG', 'SomeUnknownTag', 2)
        self.token_assert_helper(self.l.token(), 'LINE', 'SomeUnknownValue', 2)

    def token_assert_helper(self, token, ttype, value, line):
        assert token.type == ttype
        assert token.value == value
        assert token.lineno == line


class TestParser(TestCase):

    document_str = '\n'.join([
        'SPDXVersion: SPDX-2.1',
        'DataLicense: CC0-1.0',
        'DocumentName: Sample_Document-V2.1',
        'SPDXID: SPDXRef-DOCUMENT',
        'DocumentComment: <text>Sample Comment</text>',
        'DocumentNamespace: https://spdx.org/spdxdocs/spdx-example-444504E0-4F89-41D3-9A0C-0305E82C3301'
    ])

    creation_str = '\n'.join([
        'Creator: Person: Bob (bob@example.com)',
        'Creator: Organization: Acme.',
        'Created: 2010-02-03T00:00:00Z',
        'CreatorComment: <text>Sample Comment</text>'
    ])

    review_str = '\n'.join([
        'Reviewer: Person: Bob the Reviewer',
        'ReviewDate: 2010-02-10T00:00:00Z',
        'ReviewComment: <text>Bob was Here.</text>',
        'Reviewer: Person: Alice the Reviewer',
        'ReviewDate: 2011-02-10T00:00:00Z',
        'ReviewComment: <text>Alice was also here.</text>'
    ])

    package_str = '\n'.join([
        'PackageName: Test',
        'PackageVersion: Version 0.9.2',
        'PackageDownloadLocation: http://example.com/test',
        'PackageSummary: <text>Test package</text>',
        'PackageSourceInfo: <text>Version 1.0 of test</text>',
        'PackageFileName: test-1.0.zip',
        'PackageSupplier: Organization:ACME',
        'PackageOriginator: Organization:ACME',
        'PackageChecksum: SHA1: 2fd4e1c67a2d28fced849ee1bb76e7391b93eb12',
        'PackageVerificationCode: 4e3211c67a2d28fced849ee1bb76e7391b93feba (something.rdf, something.txt)',
        'PackageDescription: <text>A package.</text>',
        'PackageCopyrightText: <text> Copyright 2014 Acme Inc.</text>',
        'PackageLicenseDeclared: Apache-2.0',
        'PackageLicenseConcluded: (LicenseRef-2.0 and Apache-2.0)',
        'PackageLicenseInfoFromFiles: Apache-1.0',
        'PackageLicenseInfoFromFiles: Apache-2.0',
        'PackageLicenseComments: <text>License Comments</text>'
    ])

    file_str = '\n'.join([
        'FileName: testfile.java',
        'SPDXID: SPDXRef-File',
        'FileType: SOURCE',
        'FileChecksum: SHA1: 2fd4e1c67a2d28fced849ee1bb76e7391b93eb12',
        'LicenseConcluded: Apache-2.0',
        'LicenseInfoInFile: Apache-2.0',
        'FileCopyrightText: <text>Copyright 2014 Acme Inc.</text>',
        'ArtifactOfProjectName: AcmeTest',
        'ArtifactOfProjectHomePage: http://www.acme.org/',
        'ArtifactOfProjectURI: http://www.acme.org/',
        'FileComment: <text>Very long file</text>'
        ])

    unknown_tag_str = 'SomeUnknownTag: SomeUnknownValue'

    complete_str = '{0}\n{1}\n{2}\n{3}\n{4}'.format(document_str, creation_str, review_str, package_str, file_str)

    def setUp(self):
        self.p = Parser(Builder(), StandardLogger())
        self.p.build()

    def test_doc(self):
        document, error = self.p.parse(self.complete_str)
        assert document is not None
        assert not error
        assert document.version == Version(major=2, minor=1)
        assert document.data_license.identifier == 'CC0-1.0'
        assert document.name == 'Sample_Document-V2.1'
        assert document.spdx_id == 'SPDXRef-DOCUMENT'
        assert document.comment == 'Sample Comment'
        assert document.namespace == 'https://spdx.org/spdxdocs/spdx-example-444504E0-4F89-41D3-9A0C-0305E82C3301'

    def test_creation_info(self):
        document, error = self.p.parse(self.complete_str)
        assert document is not None
        assert not error
        assert len(document.creation_info.creators) == 2
        assert document.creation_info.comment == 'Sample Comment'
        assert (document.creation_info.created_iso_format == '2010-02-03T00:00:00Z')

    def test_review(self):
        document, error = self.p.parse(self.complete_str)
        assert document is not None
        assert not error
        assert len(document.reviews) == 2

    def test_package(self):
        document, error = self.p.parse(self.complete_str)
        assert document is not None
        assert not error
        assert document.package.name == 'Test'
        assert document.package.version == 'Version 0.9.2'
        assert len(document.package.licenses_from_files) == 2
        assert (document.package.conc_lics.identifier == 'LicenseRef-2.0 AND Apache-2.0')

    def test_file(self):
        document, error = self.p.parse(self.complete_str)
        assert document is not None
        assert not error
        assert len(document.package.files) == 1
        spdx_file = document.package.files[0]
        assert spdx_file.name == 'testfile.java'
        assert spdx_file.spdx_id == 'SPDXRef-File'
        assert spdx_file.type == spdx.file.FileType.SOURCE
        assert len(spdx_file.artifact_of_project_name) == 1
        assert len(spdx_file.artifact_of_project_home) == 1
        assert len(spdx_file.artifact_of_project_uri) == 1

    def test_unknown_tag(self):

        try:
            from StringIO import StringIO
        except ImportError:
            from io import StringIO

        saved_out = sys.stdout
        sys.stdout = StringIO()
        document, error = self.p.parse(self.unknown_tag_str)
        self.assertEqual(sys.stdout.getvalue(), 'Found unknown tag : SomeUnknownTag at line: 1\n')
        sys.stdout = saved_out
        assert error
        assert document is not None


if __name__ == '__main__':
    unittest.main()
