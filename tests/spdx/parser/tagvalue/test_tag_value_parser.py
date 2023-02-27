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
import sys
from datetime import datetime
from unittest import TestCase

import pytest
from license_expression import get_spdx_licensing

from spdx.model.actor import Actor, ActorType
from spdx.model.annotation import AnnotationType
from spdx.model.checksum import Checksum, ChecksumAlgorithm
from spdx.model.external_document_ref import ExternalDocumentRef
from spdx.model.file import FileType
from spdx.model.package import PackagePurpose, ExternalPackageRefCategory, ExternalPackageRef
from spdx.model.relationship import RelationshipType
from spdx.model.version import Version
from spdx.parser.error import SPDXParsingError
from spdx.parser.tagvalue.parser.tagvalue import Parser

document_str = '\n'.join([
    'SPDXVersion: SPDX-2.3',
    'DataLicense: CC0-1.0',
    'DocumentName: Sample_Document-V2.3',
    'SPDXID: SPDXRef-DOCUMENT',
    'DocumentComment: <text>Sample Comment</text>',
    'DocumentNamespace: https://spdx.org/spdxdocs/spdx-example-444504E0-4F89-41D3-9A0C-0305E82C3301',
    'ExternalDocumentRef: DocumentRef-spdx-tool-1.2 http://spdx.org/spdxdocs/spdx-tools-v1.2-3F2504E0-4F89-41D3-9A0C-0305E82C3301 SHA1: d6a770ba38583ed4bb4525bd96e50461655d2759'
])

creation_str = '\n'.join([
    'Creator: Person: Bob (bob@example.com)',
    'Creator: Organization: Acme.',
    'Created: 2010-02-03T00:00:00Z',
    'CreatorComment: <text>Sample Comment</text>',
    'LicenseListVersion: 3.17'
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
    'ExternalRef: OTHER LocationRef-acmeforge acmecorp/acmenator/4.1.3-alpha',
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
    'FileComment: <text>Very long file</text>',
    'FileAttributionText: <text>Acknowledgements that might be required to be communicated in some contexts.</text>'
])

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

relationship_str = '\n'.join([
    'Relationship: SPDXRef-DOCUMENT DESCRIBES SPDXRef-File',
    'RelationshipComment: This is a comment.'])

extracted_licensing_info_str = '\n'.join([
    'LicenseID: LicenseRef-Beerware-4.2',
    'ExtractedText: <text>"THE BEER-WARE LICENSE" (Revision 42): phk@FreeBSD.ORG wrote this file. As long as you retain this notice you can do whatever you want with this stuff. If we meet some day, and you think this stuff is worth it, you can buy me a beer in return Poul-Henning Kamp</text>'
    'LicenseName: Beer-Ware License (Version 42)',
    'LicenseCrossReference:  http://people.freebsd.org/~phk/',
    'LicenseComment: The beerware license has a couple of other standard variants.'
])

unknown_tag_str = 'UnknownTag: This is an example for an unknown tag.'

complete_str = '{0}\n{1}\n{2}\n{3}\n{4}\n{5}\n{6}\n{7}\n'.format(document_str, creation_str, file_str,
                                                                 annotation_str,
                                                                 relationship_str, snippet_str, package_str,
                                                                 extracted_licensing_info_str)


@pytest.fixture
def parser():
    spdx_parser = Parser()
    spdx_parser.build()
    return spdx_parser


def test_creation_info(parser):
    document = parser.parse(complete_str)
    assert document is not None
    creation_info = document.creation_info
    assert creation_info is not None
    assert creation_info.spdx_version == "SPDX-2.3"
    assert creation_info.data_license == 'CC0-1.0'
    assert creation_info.name == 'Sample_Document-V2.3'
    assert creation_info.spdx_id == 'SPDXRef-DOCUMENT'
    assert creation_info.document_comment == 'Sample Comment'
    assert creation_info.document_namespace == 'https://spdx.org/spdxdocs/spdx-example-444504E0-4F89-41D3-9A0C-0305E82C3301'
    TestCase().assertCountEqual(creation_info.creators,
                                [Actor(ActorType.PERSON, "Bob", "bob@example.com"),
                                 Actor(ActorType.ORGANIZATION, "Acme.")])
    assert creation_info.creator_comment == 'Sample Comment'
    assert creation_info.created == datetime(2010, 2, 3, 0, 0)
    assert creation_info.license_list_version == Version(3, 17)
    TestCase().assertCountEqual(creation_info.external_document_refs,
                                [ExternalDocumentRef("DocumentRef-spdx-tool-1.2",
                                                     "http://spdx.org/spdxdocs/spdx-tools-v1.2-3F2504E0-4F89-41D3-9A0C-0305E82C3301",
                                                     Checksum(ChecksumAlgorithm.SHA1,
                                                              "d6a770ba38583ed4bb4525bd96e50461655d2759"))])


def test_extracted_licensing_info(parser):
    document = parser.parse(complete_str)
    assert document is not None
    assert len(document.extracted_licensing_info) == 1
    extracted_licensing_info = document.extracted_licensing_info[0]
    assert extracted_licensing_info.license_id == "LicenseRef-Beerware-4.2"
    assert extracted_licensing_info.extracted_text == '"THE BEER-WARE LICENSE" (Revision 42): phk@FreeBSD.ORG wrote this file. As long as you retain this notice you can do whatever you want with this stuff. If we meet some day, and you think this stuff is worth it, you can buy me a beer in return Poul-Henning Kamp'
    assert extracted_licensing_info.license_name == "Beer-Ware License (Version 42)"
    assert extracted_licensing_info.cross_references == ["http://people.freebsd.org/~phk/"]
    assert extracted_licensing_info.comment == "The beerware license has a couple of other standard variants."


def test_package(parser):
    document = parser.parse(complete_str)
    assert document is not None
    package = document.packages[0]
    assert package.name == 'Test'
    assert package.spdx_id == 'SPDXRef-Package'
    assert package.version == 'Version 0.9.2'
    assert len(package.license_info_from_files) == 2
    assert package.license_concluded == get_spdx_licensing().parse('LicenseRef-2.0 AND Apache-2.0')
    assert package.files_analyzed is True
    assert package.comment == 'Comment on the package.'
    assert len(package.external_references) == 2
    TestCase().assertCountEqual(package.external_references,
                                [ExternalPackageRef(ExternalPackageRefCategory.SECURITY, "cpe23Type",
                                                    "cpe:2.3:a:pivotal_software:spring_framework:4.1.0:*:*:*:*:*:*:",
                                                    "Some comment about the package."),
                                 ExternalPackageRef(ExternalPackageRefCategory.OTHER, "LocationRef-acmeforge",
                                                    "acmecorp/acmenator/4.1.3-alpha")])
    assert package.primary_package_purpose == PackagePurpose.OPERATING_SYSTEM
    assert package.built_date == datetime(2020, 1, 1, 12, 0, 0)
    assert package.release_date == datetime(2021, 1, 1, 12, 0, 0)
    assert package.valid_until_date == datetime(2022, 1, 1, 12, 0, 0)


def test_file(parser):
    document = parser.parse(complete_str)
    assert document is not None
    assert len(document.files) == 1
    spdx_file = document.files[0]
    assert spdx_file.name == 'testfile.java'
    assert spdx_file.spdx_id == 'SPDXRef-File'
    assert spdx_file.file_type == [FileType.SOURCE, FileType.TEXT]
    assert spdx_file.comment == 'Very long file'
    assert spdx_file.attribution_texts == ['Acknowledgements that might be required to be communicated in ' \
                                           'some contexts.']
    assert spdx_file.license_info_in_file == [get_spdx_licensing().parse("Apache-2.0")]
    assert spdx_file.license_concluded == get_spdx_licensing().parse("Apache-2.0")


def test_annotation(parser):
    document = parser.parse(complete_str)
    assert document is not None
    assert len(document.annotations) == 1
    annotation = document.annotations[0]
    assert annotation.annotator.name == 'Jane Doe'
    assert annotation.annotation_date == datetime(2010, 1, 29, 18, 30, 22)
    assert annotation.annotation_comment == 'Document level annotation'
    assert annotation.annotation_type == AnnotationType.OTHER
    assert annotation.spdx_id == 'SPDXRef-DOCUMENT'


def test_relationship(parser):
    document = parser.parse(complete_str)
    assert document is not None
    relationship = document.relationships[0]
    assert relationship.relationship_type == RelationshipType.DESCRIBES
    assert relationship.related_spdx_element_id == "SPDXRef-File"
    assert relationship.spdx_element_id == "SPDXRef-DOCUMENT"
    assert relationship.comment == "This is a comment."


def test_snippet(parser):
    document = parser.parse(complete_str)
    assert document is not None
    assert len(document.snippets) == 1
    snippet = document.snippets[0]
    assert snippet.spdx_id == 'SPDXRef-Snippet'
    assert snippet.name == 'from linux kernel'
    assert snippet.comment == 'Some snippet comment.'
    assert snippet.copyright_text == ' Copyright 2008-2010 John Smith '
    assert snippet.license_comment == 'Some lic comment.'
    assert snippet.file_spdx_id == 'SPDXRef-DoapSource'
    assert snippet.license_concluded == get_spdx_licensing().parse('Apache-2.0')
    assert snippet.license_info_in_snippet == [get_spdx_licensing().parse('Apache-2.0')]
    assert snippet.byte_range[0] == 310
    assert snippet.byte_range[1] == 420
    assert snippet.line_range[0] == 5
    assert snippet.line_range[1] == 23


def test_unknown_str(parser):
    with pytest.raises(SPDXParsingError, match="Unknown tag"):
        parser.parse(unknown_tag_str)
