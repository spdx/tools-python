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

import sys
from datetime import datetime
from unittest import TestCase

import spdx
from spdx import utils
from spdx.package import PackagePurpose
from spdx.parsers.tagvalue import Parser
from spdx.parsers.lexers.tagvalue import Lexer
from spdx.parsers.tagvaluebuilders import Builder
from spdx.parsers.loggers import StandardLogger
from spdx.version import Version

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
    'SPDXID: SPDXRef-Package',
    'PackageVersion: Version 0.9.2',
    'PackageDownloadLocation: http://example.com/test',
    'FilesAnalyzed: True',
    'PackageSummary: <text>Test package</text>',
    'PackageSourceInfo: <text>Version 1.0 of test</text>',
    'PackageFileName: test-1.0.zip',
    'PackageSupplier: Organization:ACME',
    'PackageOriginator: Organization:ACME',
    'PackageChecksum: SHA1: 2fd4e1c67a2d28fced849ee1bb76e7391b93eb12',
    'PackageVerificationCode: 4e3211c67a2d28fced849ee1bb76e7391b93feba (something.rdf, something.txt)',
    'PackageDescription: <text>A package.</text>',
    'PackageComment: <text>Comment on the package.</text>',
    'PackageCopyrightText: <text> Copyright 2014 Acme Inc.</text>',
    'PackageLicenseDeclared: Apache-2.0',
    'PackageLicenseConcluded: (LicenseRef-2.0 and Apache-2.0)',
    'PackageLicenseInfoFromFiles: Apache-1.0',
    'PackageLicenseInfoFromFiles: Apache-2.0',
    'PackageLicenseComments: <text>License Comments</text>',
    'ExternalRef: SECURITY cpe23Type cpe:2.3:a:pivotal_software:spring_framework:4.1.0:*:*:*:*:*:*:',
    'ExternalRefComment: <text>Some comment about the package.</text>',
    'PrimaryPackagePurpose: OPERATING-SYSTEM',
    'BuiltDate: 2020-01-01T12:00:00Z',
    'ReleaseDate: 2021-01-01T12:00:00Z',
    'ValidUntilDate: 2022-01-01T12:00:00Z'
])

file_str = '\n'.join([
    'FileName: testfile.java',
    'SPDXID: SPDXRef-File',
    'FileType: SOURCE',
    'FileType: TEXT',
    'FileChecksum: SHA1: 2fd4e1c67a2d28fced849ee1bb76e7391b93eb12',
    'LicenseConcluded: Apache-2.0',
    'LicenseInfoInFile: Apache-2.0',
    'FileCopyrightText: <text>Copyright 2014 Acme Inc.</text>',
    'ArtifactOfProjectName: AcmeTest',
    'ArtifactOfProjectHomePage: http://www.acme.org/',
    'ArtifactOfProjectURI: http://www.acme.org/',
    'FileComment: <text>Very long file</text>',
    'FileAttributionText: <text>Acknowledgements that might be required to be communicated in some contexts.</text>'
        ])

unknown_tag_str = 'SomeUnknownTag: SomeUnknownValue'

snippet_str = '\n'.join([
    'SnippetSPDXID: SPDXRef-Snippet',
    'SnippetLicenseComments: <text>Some lic comment.</text>',
    'SnippetCopyrightText: <text> Copyright 2008-2010 John Smith </text>',
    'SnippetComment: <text>Some snippet comment.</text>',
    'SnippetName: from linux kernel',
    'SnippetFromFileSPDXID: SPDXRef-DoapSource',
    'SnippetLicenseConcluded: Apache-2.0',
    'LicenseInfoInSnippet: Apache-2.0',
    'SnippetByteRange: 310:420',
    'SnippetLineRange: 5:23',
])

annotation_str = '\n'.join([
    'Annotator: Person: Jane Doe()',
    'AnnotationDate: 2010-01-29T18:30:22Z',
    'AnnotationComment: <text>Document level annotation</text>',
    'AnnotationType: OTHER',
    'SPDXREF: SPDXRef-DOCUMENT'
])


class TestLexer(TestCase):
    maxDiff = None

    def setUp(self):
        self.l = Lexer()
        self.l.build()

    def test_document(self):
        data = document_str
        self.l.input(data)
        self.token_assert_helper(self.l.token(), 'DOC_VERSION', 'SPDXVersion', 1)
        self.token_assert_helper(self.l.token(), 'LINE', 'SPDX-2.1', 1)
        self.token_assert_helper(self.l.token(), 'DOC_LICENSE', 'DataLicense', 2)
        self.token_assert_helper(self.l.token(), 'LINE', 'CC0-1.0', 2)
        self.token_assert_helper(self.l.token(), 'DOC_NAME', 'DocumentName', 3)
        self.token_assert_helper(self.l.token(), 'LINE', 'Sample_Document-V2.1',
                                 3)
        self.token_assert_helper(self.l.token(), 'SPDX_ID', 'SPDXID', 4)
        self.token_assert_helper(self.l.token(), 'LINE', 'SPDXRef-DOCUMENT', 4)
        self.token_assert_helper(self.l.token(), 'DOC_COMMENT', 'DocumentComment', 5)
        self.token_assert_helper(self.l.token(), 'TEXT', '<text>Sample Comment</text>', 5)
        self.token_assert_helper(self.l.token(), 'DOC_NAMESPACE',
                                 'DocumentNamespace', 6)
        self.token_assert_helper(self.l.token(), 'LINE',
                                 'https://spdx.org/spdxdocs/spdx-example-444504E0-4F89-41D3-9A0C-0305E82C3301',
                                 6)

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
        data = creation_str
        self.l.input(data)
        self.token_assert_helper(self.l.token(), 'CREATOR', 'Creator', 1)
        self.token_assert_helper(self.l.token(), 'PERSON_VALUE', "Person: Bob (bob@example.com)", 1)
        self.token_assert_helper(self.l.token(), 'CREATOR', 'Creator', 2)
        self.token_assert_helper(self.l.token(), 'ORG_VALUE', 'Organization: Acme.', 2)
        self.token_assert_helper(self.l.token(), 'CREATED', 'Created', 3)
        self.token_assert_helper(self.l.token(), 'DATE', '2010-02-03T00:00:00Z', 3)
        self.token_assert_helper(self.l.token(), 'CREATOR_COMMENT', 'CreatorComment', 4)
        self.token_assert_helper(self.l.token(), 'TEXT', '<text>Sample Comment</text>', 4)

    def test_review_info(self):
        data = review_str
        self.l.input(data)
        self.token_assert_helper(self.l.token(), 'REVIEWER', 'Reviewer', 1)
        self.token_assert_helper(self.l.token(), 'PERSON_VALUE', "Person: Bob the Reviewer", 1)
        self.token_assert_helper(self.l.token(), 'REVIEW_DATE', 'ReviewDate', 2)
        self.token_assert_helper(self.l.token(), 'DATE', '2010-02-10T00:00:00Z', 2)
        self.token_assert_helper(self.l.token(), 'REVIEW_COMMENT', 'ReviewComment', 3)
        self.token_assert_helper(self.l.token(), 'TEXT', '<text>Bob was Here.</text>', 3)
        self.token_assert_helper(self.l.token(), 'REVIEWER', 'Reviewer', 4)
        self.token_assert_helper(self.l.token(), 'PERSON_VALUE', "Person: Alice the Reviewer", 4)
        self.token_assert_helper(self.l.token(), 'REVIEW_DATE', 'ReviewDate', 5)
        self.token_assert_helper(self.l.token(), 'DATE', '2011-02-10T00:00:00Z', 5)
        self.token_assert_helper(self.l.token(), 'REVIEW_COMMENT', 'ReviewComment', 6)
        self.token_assert_helper(self.l.token(), 'TEXT', '<text>Alice was also here.</text>', 6)

    def test_package(self):
        data = package_str
        self.l.input(data)
        self.token_assert_helper(self.l.token(), 'PKG_NAME', 'PackageName', 1)
        self.token_assert_helper(self.l.token(), 'LINE', 'Test', 1)
        self.token_assert_helper(self.l.token(), 'SPDX_ID', 'SPDXID', 2)
        self.token_assert_helper(self.l.token(), 'LINE', 'SPDXRef-Package', 2)
        self.token_assert_helper(self.l.token(), 'PKG_VERSION', 'PackageVersion', 3)
        self.token_assert_helper(self.l.token(), 'LINE', 'Version 0.9.2', 3)
        self.token_assert_helper(self.l.token(), 'PKG_DOWN', 'PackageDownloadLocation', 4)
        self.token_assert_helper(self.l.token(), 'LINE', 'http://example.com/test', 4)
        self.token_assert_helper(self.l.token(), 'PKG_FILES_ANALYZED', 'FilesAnalyzed', 5)
        self.token_assert_helper(self.l.token(), 'LINE', 'True', 5)
        self.token_assert_helper(self.l.token(), 'PKG_SUM', 'PackageSummary', 6)
        self.token_assert_helper(self.l.token(), 'TEXT', '<text>Test package</text>', 6)
        self.token_assert_helper(self.l.token(), 'PKG_SRC_INFO', 'PackageSourceInfo', 7)
        self.token_assert_helper(self.l.token(), 'TEXT', '<text>Version 1.0 of test</text>', 7)
        self.token_assert_helper(self.l.token(), 'PKG_FILE_NAME', 'PackageFileName', 8)
        self.token_assert_helper(self.l.token(), 'LINE', 'test-1.0.zip', 8)
        self.token_assert_helper(self.l.token(), 'PKG_SUPPL', 'PackageSupplier', 9)
        self.token_assert_helper(self.l.token(), 'ORG_VALUE', 'Organization:ACME', 9)
        self.token_assert_helper(self.l.token(), 'PKG_ORIG', 'PackageOriginator', 10)
        self.token_assert_helper(self.l.token(), 'ORG_VALUE', 'Organization:ACME', 10)
        self.token_assert_helper(self.l.token(), 'PKG_CHKSUM', 'PackageChecksum', 11)
        self.token_assert_helper(self.l.token(), 'CHKSUM', 'SHA1: 2fd4e1c67a2d28fced849ee1bb76e7391b93eb12', 11)
        self.token_assert_helper(self.l.token(), 'PKG_VERF_CODE', 'PackageVerificationCode', 12)
        self.token_assert_helper(self.l.token(), 'LINE', '4e3211c67a2d28fced849ee1bb76e7391b93feba (something.rdf, something.txt)', 12)
        self.token_assert_helper(self.l.token(), 'PKG_DESC', 'PackageDescription', 13)
        self.token_assert_helper(self.l.token(), 'TEXT', '<text>A package.</text>', 13)
        self.token_assert_helper(self.l.token(), 'PKG_COMMENT', 'PackageComment', 14)
        self.token_assert_helper(self.l.token(), 'TEXT', '<text>Comment on the package.</text>', 14)
        self.token_assert_helper(self.l.token(), 'PKG_CPY_TEXT', 'PackageCopyrightText', 15)
        self.token_assert_helper(self.l.token(), 'TEXT', '<text> Copyright 2014 Acme Inc.</text>', 15)
        self.token_assert_helper(self.l.token(), 'PKG_LICS_DECL', 'PackageLicenseDeclared', 16)
        self.token_assert_helper(self.l.token(), 'LINE', 'Apache-2.0', 16)
        self.token_assert_helper(self.l.token(), 'PKG_LICS_CONC', 'PackageLicenseConcluded', 17)
        self.token_assert_helper(self.l.token(), 'LINE', '(LicenseRef-2.0 and Apache-2.0)', 17)
        self.token_assert_helper(self.l.token(), 'PKG_LICS_FFILE', 'PackageLicenseInfoFromFiles', 18)
        self.token_assert_helper(self.l.token(), 'LINE', 'Apache-1.0', 18)
        self.token_assert_helper(self.l.token(), 'PKG_LICS_FFILE', 'PackageLicenseInfoFromFiles', 19)
        self.token_assert_helper(self.l.token(), 'LINE', 'Apache-2.0', 19)
        self.token_assert_helper(self.l.token(), 'PKG_LICS_COMMENT', 'PackageLicenseComments', 20)
        self.token_assert_helper(self.l.token(), 'TEXT', '<text>License Comments</text>', 20)
        self.token_assert_helper(self.l.token(), 'PKG_EXT_REF', 'ExternalRef', 21)
        self.token_assert_helper(self.l.token(), 'LINE', 'SECURITY cpe23Type cpe:2.3:a:pivotal_software:spring_framework:4.1.0:*:*:*:*:*:*:', 21)
        self.token_assert_helper(self.l.token(), 'PKG_EXT_REF_COMMENT', 'ExternalRefComment', 22)
        self.token_assert_helper(self.l.token(), 'TEXT', '<text>Some comment about the package.</text>', 22)
        self.token_assert_helper(self.l.token(), 'PRIMARY_PACKAGE_PURPOSE', 'PrimaryPackagePurpose', 23)
        self.token_assert_helper(self.l.token(), 'OPERATING_SYSTEM', 'OPERATING-SYSTEM', 23)
        self.token_assert_helper(self.l.token(), 'BUILT_DATE', 'BuiltDate', 24)
        self.token_assert_helper(self.l.token(), 'DATE', '2020-01-01T12:00:00Z', 24)
        self.token_assert_helper(self.l.token(), 'RELEASE_DATE', 'ReleaseDate', 25)
        self.token_assert_helper(self.l.token(), 'DATE', '2021-01-01T12:00:00Z', 25)
        self.token_assert_helper(self.l.token(), 'VALID_UNTIL_DATE', 'ValidUntilDate', 26)
        self.token_assert_helper(self.l.token(), 'DATE', '2022-01-01T12:00:00Z', 26)


    def test_unknown_tag(self):
        data = unknown_tag_str
        self.l.input(data)
        self.token_assert_helper(self.l.token(), 'UNKNOWN_TAG', 'SomeUnknownTag', 1)
        self.token_assert_helper(self.l.token(), 'LINE', 'SomeUnknownValue', 1)

    def test_snippet(self):
        data = snippet_str
        self.l.input(data)
        self.token_assert_helper(self.l.token(), 'SNIPPET_SPDX_ID', 'SnippetSPDXID', 1)
        self.token_assert_helper(self.l.token(), 'LINE', 'SPDXRef-Snippet', 1)
        self.token_assert_helper(self.l.token(), 'SNIPPET_LICS_COMMENT', 'SnippetLicenseComments', 2)
        self.token_assert_helper(self.l.token(), 'TEXT', '<text>Some lic comment.</text>', 2)
        self.token_assert_helper(self.l.token(), 'SNIPPET_CR_TEXT', 'SnippetCopyrightText', 3)
        self.token_assert_helper(self.l.token(), 'TEXT', '<text> Copyright 2008-2010 John Smith </text>', 3)
        self.token_assert_helper(self.l.token(), 'SNIPPET_COMMENT', 'SnippetComment', 4)
        self.token_assert_helper(self.l.token(), 'TEXT', '<text>Some snippet comment.</text>', 4)
        self.token_assert_helper(self.l.token(), 'SNIPPET_NAME', 'SnippetName', 5)
        self.token_assert_helper(self.l.token(), 'LINE', 'from linux kernel', 5)
        self.token_assert_helper(self.l.token(), 'SNIPPET_FILE_SPDXID',
                                 'SnippetFromFileSPDXID', 6)
        self.token_assert_helper(self.l.token(), 'LINE', 'SPDXRef-DoapSource', 6)
        self.token_assert_helper(self.l.token(), 'SNIPPET_LICS_CONC',
                                 'SnippetLicenseConcluded', 7)
        self.token_assert_helper(self.l.token(), 'LINE', 'Apache-2.0', 7)
        self.token_assert_helper(self.l.token(), 'SNIPPET_LICS_INFO',
                                 'LicenseInfoInSnippet', 8)
        self.token_assert_helper(self.l.token(), 'LINE', 'Apache-2.0', 8)
        self.token_assert_helper(self.l.token(), 'SNIPPET_BYTE_RANGE', 'SnippetByteRange', 9)
        self.token_assert_helper(self.l.token(), 'RANGE', '310:420', 9)
        self.token_assert_helper(self.l.token(), 'SNIPPET_LINE_RANGE', 'SnippetLineRange', 10)
        self.token_assert_helper(self.l.token(), 'RANGE', '5:23', 10)

    def test_annotation(self):
        data = annotation_str
        self.l.input(data)
        self.token_assert_helper(self.l.token(), 'ANNOTATOR', 'Annotator', 1)
        self.token_assert_helper(self.l.token(), 'PERSON_VALUE', 'Person: Jane Doe()', 1)
        self.token_assert_helper(self.l.token(), 'ANNOTATION_DATE', 'AnnotationDate', 2)
        self.token_assert_helper(self.l.token(), 'DATE', '2010-01-29T18:30:22Z', 2)
        self.token_assert_helper(self.l.token(), 'ANNOTATION_COMMENT', 'AnnotationComment', 3)
        self.token_assert_helper(self.l.token(), 'TEXT', '<text>Document level annotation</text>', 3)
        self.token_assert_helper(self.l.token(), 'ANNOTATION_TYPE', 'AnnotationType', 4)
        self.token_assert_helper(self.l.token(), 'OTHER', 'OTHER', 4)
        self.token_assert_helper(self.l.token(), 'ANNOTATION_SPDX_ID', 'SPDXREF', 5)
        self.token_assert_helper(self.l.token(), 'LINE', 'SPDXRef-DOCUMENT', 5)

    def token_assert_helper(self, token, ttype, value, line):
        assert token.type == ttype
        assert token.value == value
        assert token.lineno == line


class TestParser(TestCase):
    maxDiff = None
    complete_str = '{0}\n{1}\n{2}\n{3}\n{4}\n{5}\n{6}'.format(document_str, creation_str, review_str, package_str,
                                                              file_str, annotation_str, snippet_str)

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
        assert document.package.spdx_id == 'SPDXRef-Package'
        assert document.package.version == 'Version 0.9.2'
        assert len(document.package.licenses_from_files) == 2
        assert (document.package.conc_lics.identifier == 'LicenseRef-2.0 AND Apache-2.0')
        assert document.package.files_analyzed is True
        assert document.package.comment == 'Comment on the package.'
        assert document.package.pkg_ext_refs[-1].category == 'SECURITY'
        assert document.package.pkg_ext_refs[-1].pkg_ext_ref_type == 'cpe23Type'
        assert document.package.pkg_ext_refs[-1].locator == 'cpe:2.3:a:pivotal_software:spring_framework:4.1.0:*:*:*:*:*:*:'
        assert document.package.pkg_ext_refs[-1].comment == 'Some comment about the package.'
        assert document.package.primary_package_purpose == PackagePurpose.OPERATING_SYSTEM
        assert document.package.built_date == datetime(2020, 1, 1, 12, 0, 0)
        assert document.package.release_date == datetime(2021, 1, 1, 12, 0, 0)
        assert document.package.valid_until_date == datetime(2022, 1, 1, 12, 0, 0)

    def test_file(self):
        document, error = self.p.parse(self.complete_str)
        assert document is not None
        assert not error
        assert len(document.files) == 1
        spdx_file = document.files[0]
        assert spdx_file.name == 'testfile.java'
        assert spdx_file.spdx_id == 'SPDXRef-File'
        assert spdx_file.file_types == [spdx.file.FileType.SOURCE, spdx.file.FileType.TEXT]
        assert len(spdx_file.artifact_of_project_name) == 1
        assert len(spdx_file.artifact_of_project_home) == 1
        assert len(spdx_file.artifact_of_project_uri) == 1
        assert spdx_file.comment == 'Very long file'
        assert spdx_file.attribution_text == 'Acknowledgements that might be required to be communicated in ' \
                                             'some contexts.'

    def test_annotation(self):
        document, error = self.p.parse(self.complete_str)
        assert document is not None
        assert not error
        assert len(document.annotations) == 1
        assert document.annotations[-1].annotator.name == 'Jane Doe'
        assert spdx.utils.datetime_iso_format(document.annotations[-1].annotation_date) == '2010-01-29T18:30:22Z'
        assert document.annotations[-1].comment == 'Document level annotation'
        assert document.annotations[-1].annotation_type == 'OTHER'
        assert document.annotations[-1].spdx_id == 'SPDXRef-DOCUMENT'

    def test_unknown_tag(self):
        try:
            from StringIO import StringIO
        except ImportError:
            from io import StringIO

        saved_out = sys.stdout
        sys.stdout = StringIO()
        document, error = self.p.parse(unknown_tag_str)
        self.assertEqual(sys.stdout.getvalue(), 'Found unknown tag : SomeUnknownTag at line: 1\n')
        sys.stdout = saved_out
        assert error
        assert document is not None

    def test_snippet(self):
        document, error = self.p.parse(self.complete_str)
        assert document is not None
        assert not error
        assert len(document.snippet) == 1
        assert document.snippet[-1].spdx_id == 'SPDXRef-Snippet'
        assert document.snippet[-1].name == 'from linux kernel'
        assert document.snippet[-1].comment == 'Some snippet comment.'
        assert document.snippet[-1].copyright == ' Copyright 2008-2010 John Smith '
        assert document.snippet[-1].license_comment == 'Some lic comment.'
        assert document.snippet[-1].snip_from_file_spdxid == 'SPDXRef-DoapSource'
        assert document.snippet[-1].conc_lics.identifier == 'Apache-2.0'
        assert document.snippet[-1].licenses_in_snippet[-1].identifier == 'Apache-2.0'
        assert document.snippet[-1].byte_range[0] == 310
        assert document.snippet[-1].byte_range[1] == 420
        assert document.snippet[-1].line_range[0] == 5
        assert document.snippet[-1].line_range[1] == 23
