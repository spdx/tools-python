# Copyright (c) 2014 Ahmed H. Ismail
# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import pytest

from spdx_tools.spdx.constants import DOCUMENT_SPDX_ID
from spdx_tools.spdx.parser.tagvalue.lexer import SPDXLexer


@pytest.fixture
def lexer():
    lexer = SPDXLexer()
    lexer.build()
    return lexer


def token_assert_helper(token, token_type, value, line_number):
    assert token.type == token_type
    assert token.value == value
    assert token.lineno == line_number


def test_tokenization_of_document(lexer):
    document_str = "\n".join(
        [
            "SPDXVersion: SPDX-2.1",
            "DataLicense: CC0-1.0",
            "DocumentName: Sample_Document-V2.1",
            f"SPDXID: {DOCUMENT_SPDX_ID}",
            "DocumentComment: <text>Sample Comment</text>",
            "DocumentNamespace: https://spdx.org/spdxdocs/spdx-example-444504E0-4F89-41D3-9A0C-0305E82C3301",
        ]
    )
    lexer.input(document_str)
    token_assert_helper(lexer.token(), "DOC_VERSION", "SPDXVersion", 1)
    token_assert_helper(lexer.token(), "LINE", "SPDX-2.1", 1)
    token_assert_helper(lexer.token(), "DOC_LICENSE", "DataLicense", 2)
    token_assert_helper(lexer.token(), "LINE", "CC0-1.0", 2)
    token_assert_helper(lexer.token(), "DOC_NAME", "DocumentName", 3)
    token_assert_helper(lexer.token(), "LINE", "Sample_Document-V2.1", 3)
    token_assert_helper(lexer.token(), "SPDX_ID", "SPDXID", 4)
    token_assert_helper(lexer.token(), "LINE", DOCUMENT_SPDX_ID, 4)
    token_assert_helper(lexer.token(), "DOC_COMMENT", "DocumentComment", 5)
    token_assert_helper(lexer.token(), "TEXT", "<text>Sample Comment</text>", 5)
    token_assert_helper(lexer.token(), "DOC_NAMESPACE", "DocumentNamespace", 6)
    token_assert_helper(
        lexer.token(), "LINE", "https://spdx.org/spdxdocs/spdx-example-444504E0-4F89-41D3-9A0C-0305E82C3301", 6
    )


def test_tokenization_of_external_document_references(lexer):
    data = "\n".join(
        [
            "ExternalDocumentRef:DocumentRef-spdx-tool-2.1 http://spdx.org/spdxdocs/spdx-tools-v2.1-3F2504E0-4F89-41D3"
            "-9A0C-0305E82C3301 SHA1: d6a770ba38583ed4bb4525bd96e50461655d2759",
            "ExternalDocumentRef:DocumentRef-spdx-tool-2.1 ldap://[2001:db8::7]/c=GB?objectClass?one "
            "SHA1: d6a770ba38583ed4bb4525bd96e50461655d2759",
        ]
    )
    lexer.input(data)
    token_assert_helper(lexer.token(), "EXT_DOC_REF", "ExternalDocumentRef", 1)
    token_assert_helper(
        lexer.token(),
        "LINE",
        "DocumentRef-spdx-tool-2.1 http://spdx.org/spdxdocs/spdx-tools-v2.1-3F2504E0-4F89-41D3-9A0C-0305E82C3301 "
        "SHA1: d6a770ba38583ed4bb4525bd96e50461655d2759",
        1,
    )
    token_assert_helper(lexer.token(), "EXT_DOC_REF", "ExternalDocumentRef", 2)
    token_assert_helper(
        lexer.token(),
        "LINE",
        "DocumentRef-spdx-tool-2.1 ldap://[2001:db8::7]/c=GB?objectClass?one "
        "SHA1: d6a770ba38583ed4bb4525bd96e50461655d2759",
        2,
    )


def test_tokenization_of_file(lexer):
    file_str = "\n".join(
        [
            "FileName: testfile.java",
            "SPDXID: SPDXRef-File",
            "FileType: SOURCE",
            "FileType: TEXT",
            "FileChecksum: SHA1: 2fd4e1c67a2d28fced849ee1bb76e7391b93eb12",
            "LicenseConcluded: Apache-2.0",
            "LicenseInfoInFile: Apache-2.0",
            "FileCopyrightText: <text>Copyright 2014 Acme Inc.</text>",
            "FileComment: <text>Very long file</text>",
            "FileAttributionText: <text>Acknowledgements that might be required to be communicated in some contexts."
            "</text>",
        ]
    )

    lexer.input(file_str)
    token_assert_helper(lexer.token(), "FILE_NAME", "FileName", 1)
    token_assert_helper(lexer.token(), "LINE", "testfile.java", 1)
    token_assert_helper(lexer.token(), "SPDX_ID", "SPDXID", 2)
    token_assert_helper(lexer.token(), "LINE", "SPDXRef-File", 2)
    token_assert_helper(lexer.token(), "FILE_TYPE", "FileType", 3)
    token_assert_helper(lexer.token(), "LINE", "SOURCE", 3)
    token_assert_helper(lexer.token(), "FILE_TYPE", "FileType", 4)
    token_assert_helper(lexer.token(), "LINE", "TEXT", 4)
    token_assert_helper(lexer.token(), "FILE_CHECKSUM", "FileChecksum", 5)
    token_assert_helper(lexer.token(), "CHECKSUM", "SHA1: 2fd4e1c67a2d28fced849ee1bb76e7391b93eb12", 5)
    token_assert_helper(lexer.token(), "FILE_LICENSE_CONCLUDED", "LicenseConcluded", 6)
    token_assert_helper(lexer.token(), "LINE", "Apache-2.0", 6)
    token_assert_helper(lexer.token(), "FILE_LICENSE_INFO", "LicenseInfoInFile", 7)
    token_assert_helper(lexer.token(), "LINE", "Apache-2.0", 7)
    token_assert_helper(lexer.token(), "FILE_COPYRIGHT_TEXT", "FileCopyrightText", 8)
    token_assert_helper(lexer.token(), "TEXT", "<text>Copyright 2014 Acme Inc.</text>", 8)
    token_assert_helper(lexer.token(), "FILE_COMMENT", "FileComment", 9)
    token_assert_helper(lexer.token(), "TEXT", "<text>Very long file</text>", 9)
    token_assert_helper(lexer.token(), "FILE_ATTRIBUTION_TEXT", "FileAttributionText", 10)
    token_assert_helper(
        lexer.token(),
        "TEXT",
        "<text>Acknowledgements that might be required to be communicated in some contexts.</text>",
        10,
    )


def test_tokenization_of_creation_info(lexer):
    creation_str = "\n".join(
        [
            "Creator: Person: Bob (bob@example.com)",
            "Creator: Organization: Acme.",
            "Created: 2010-02-03T00:00:00Z",
            "CreatorComment: <text>Sample Comment</text>",
        ]
    )

    lexer.input(creation_str)
    token_assert_helper(lexer.token(), "CREATOR", "Creator", 1)
    token_assert_helper(lexer.token(), "PERSON_VALUE", "Person: Bob (bob@example.com)", 1)
    token_assert_helper(lexer.token(), "CREATOR", "Creator", 2)
    token_assert_helper(lexer.token(), "ORGANIZATION_VALUE", "Organization: Acme.", 2)
    token_assert_helper(lexer.token(), "CREATED", "Created", 3)
    token_assert_helper(lexer.token(), "ISO8601_DATE", "2010-02-03T00:00:00Z", 3)
    token_assert_helper(lexer.token(), "CREATOR_COMMENT", "CreatorComment", 4)
    token_assert_helper(lexer.token(), "TEXT", "<text>Sample Comment</text>", 4)


def test_tokenization_of_package(lexer):
    package_str = "\n".join(
        [
            "PackageName: Test",
            "SPDXID: SPDXRef-Package",
            "PackageVersion: Version 0.9.2",
            "PackageDownloadLocation: http://example.com/test",
            "FilesAnalyzed: True",
            "PackageSummary: <text>Test package</text>",
            "PackageSourceInfo: <text>Version 1.0 of test</text>",
            "PackageFileName: test-1.0.zip",
            "PackageSupplier: Organization:ACME",
            "PackageOriginator: Organization:ACME",
            "PackageChecksum: SHA1: 2fd4e1c67a2d28fced849ee1bb76e7391b93eb12",
            "PackageVerificationCode: 4e3211c67a2d28fced849ee1bb76e7391b93feba (something.rdf, something.txt)",
            "PackageDescription: <text>A package.</text>",
            "PackageComment: <text>Comment on the package.</text>",
            "PackageCopyrightText: <text> Copyright 2014 Acme Inc.</text>",
            "PackageLicenseDeclared: Apache-2.0",
            "PackageLicenseConcluded: (LicenseRef-2.0 and Apache-2.0)",
            "PackageLicenseInfoFromFiles: Apache-1.0",
            "PackageLicenseInfoFromFiles: Apache-2.0",
            "PackageLicenseComments: <text>License Comments</text>",
            "ExternalRef: SECURITY cpe23Type cpe:2.3:a:pivotal_software:spring_framework:4.1.0:*:*:*:*:*:*:",
            "ExternalRefComment: <text>Some comment about the package.</text>",
            "PrimaryPackagePurpose: OPERATING-SYSTEM",
            "BuiltDate: 2020-01-01T12:00:00Z",
            "ReleaseDate: 2021-01-01T12:00:00Z",
            "ValidUntilDate: 2022-01-01T12:00:00Z",
        ]
    )

    lexer.input(package_str)
    token_assert_helper(lexer.token(), "PKG_NAME", "PackageName", 1)
    token_assert_helper(lexer.token(), "LINE", "Test", 1)
    token_assert_helper(lexer.token(), "SPDX_ID", "SPDXID", 2)
    token_assert_helper(lexer.token(), "LINE", "SPDXRef-Package", 2)
    token_assert_helper(lexer.token(), "PKG_VERSION", "PackageVersion", 3)
    token_assert_helper(lexer.token(), "LINE", "Version 0.9.2", 3)
    token_assert_helper(lexer.token(), "PKG_DOWNLOAD_LOCATION", "PackageDownloadLocation", 4)
    token_assert_helper(lexer.token(), "LINE", "http://example.com/test", 4)
    token_assert_helper(lexer.token(), "PKG_FILES_ANALYZED", "FilesAnalyzed", 5)
    token_assert_helper(lexer.token(), "LINE", "True", 5)
    token_assert_helper(lexer.token(), "PKG_SUMMARY", "PackageSummary", 6)
    token_assert_helper(lexer.token(), "TEXT", "<text>Test package</text>", 6)
    token_assert_helper(lexer.token(), "PKG_SOURCE_INFO", "PackageSourceInfo", 7)
    token_assert_helper(lexer.token(), "TEXT", "<text>Version 1.0 of test</text>", 7)
    token_assert_helper(lexer.token(), "PKG_FILE_NAME", "PackageFileName", 8)
    token_assert_helper(lexer.token(), "LINE", "test-1.0.zip", 8)
    token_assert_helper(lexer.token(), "PKG_SUPPLIER", "PackageSupplier", 9)
    token_assert_helper(lexer.token(), "ORGANIZATION_VALUE", "Organization:ACME", 9)
    token_assert_helper(lexer.token(), "PKG_ORIGINATOR", "PackageOriginator", 10)
    token_assert_helper(lexer.token(), "ORGANIZATION_VALUE", "Organization:ACME", 10)
    token_assert_helper(lexer.token(), "PKG_CHECKSUM", "PackageChecksum", 11)
    token_assert_helper(lexer.token(), "CHECKSUM", "SHA1: 2fd4e1c67a2d28fced849ee1bb76e7391b93eb12", 11)
    token_assert_helper(lexer.token(), "PKG_VERIFICATION_CODE", "PackageVerificationCode", 12)
    token_assert_helper(
        lexer.token(), "LINE", "4e3211c67a2d28fced849ee1bb76e7391b93feba (something.rdf, something.txt)", 12
    )
    token_assert_helper(lexer.token(), "PKG_DESCRIPTION", "PackageDescription", 13)
    token_assert_helper(lexer.token(), "TEXT", "<text>A package.</text>", 13)
    token_assert_helper(lexer.token(), "PKG_COMMENT", "PackageComment", 14)
    token_assert_helper(lexer.token(), "TEXT", "<text>Comment on the package.</text>", 14)
    token_assert_helper(lexer.token(), "PKG_COPYRIGHT_TEXT", "PackageCopyrightText", 15)
    token_assert_helper(lexer.token(), "TEXT", "<text> Copyright 2014 Acme Inc.</text>", 15)
    token_assert_helper(lexer.token(), "PKG_LICENSE_DECLARED", "PackageLicenseDeclared", 16)
    token_assert_helper(lexer.token(), "LINE", "Apache-2.0", 16)
    token_assert_helper(lexer.token(), "PKG_LICENSE_CONCLUDED", "PackageLicenseConcluded", 17)
    token_assert_helper(lexer.token(), "LINE", "(LicenseRef-2.0 and Apache-2.0)", 17)
    token_assert_helper(lexer.token(), "PKG_LICENSE_INFO", "PackageLicenseInfoFromFiles", 18)
    token_assert_helper(lexer.token(), "LINE", "Apache-1.0", 18)
    token_assert_helper(lexer.token(), "PKG_LICENSE_INFO", "PackageLicenseInfoFromFiles", 19)
    token_assert_helper(lexer.token(), "LINE", "Apache-2.0", 19)
    token_assert_helper(lexer.token(), "PKG_LICENSE_COMMENT", "PackageLicenseComments", 20)
    token_assert_helper(lexer.token(), "TEXT", "<text>License Comments</text>", 20)
    token_assert_helper(lexer.token(), "PKG_EXTERNAL_REF", "ExternalRef", 21)
    token_assert_helper(
        lexer.token(), "LINE", "SECURITY cpe23Type cpe:2.3:a:pivotal_software:spring_framework:4.1.0:*:*:*:*:*:*:", 21
    )
    token_assert_helper(lexer.token(), "PKG_EXTERNAL_REF_COMMENT", "ExternalRefComment", 22)
    token_assert_helper(lexer.token(), "TEXT", "<text>Some comment about the package.</text>", 22)
    token_assert_helper(lexer.token(), "PRIMARY_PACKAGE_PURPOSE", "PrimaryPackagePurpose", 23)
    token_assert_helper(lexer.token(), "LINE", "OPERATING-SYSTEM", 23)
    token_assert_helper(lexer.token(), "BUILT_DATE", "BuiltDate", 24)
    token_assert_helper(lexer.token(), "ISO8601_DATE", "2020-01-01T12:00:00Z", 24)
    token_assert_helper(lexer.token(), "RELEASE_DATE", "ReleaseDate", 25)
    token_assert_helper(lexer.token(), "ISO8601_DATE", "2021-01-01T12:00:00Z", 25)
    token_assert_helper(lexer.token(), "VALID_UNTIL_DATE", "ValidUntilDate", 26)
    token_assert_helper(lexer.token(), "ISO8601_DATE", "2022-01-01T12:00:00Z", 26)


def test_tokenization_of_unknown_tag(lexer):
    unknown_tag_str = "SomeUnknownTag: SomeUnknownValue"
    lexer.input(unknown_tag_str)
    token_assert_helper(lexer.token(), "UNKNOWN_TAG", "SomeUnknownTag", 1)
    token_assert_helper(lexer.token(), "LINE", "SomeUnknownValue", 1)


def test_tokenization_of_snippet(lexer):
    snippet_str = "\n".join(
        [
            "SnippetSPDXID: SPDXRef-Snippet",
            "SnippetLicenseComments: <text>Some lic comment.</text>",
            "SnippetCopyrightText: <text> Copyright 2008-2010 John Smith </text>",
            "SnippetComment: <text>Some snippet comment.</text>",
            "SnippetName: from linux kernel",
            "SnippetFromFileSPDXID: SPDXRef-DoapSource",
            "SnippetLicenseConcluded: Apache-2.0",
            "LicenseInfoInSnippet: Apache-2.0",
            "SnippetByteRange: 310:420",
            "SnippetLineRange: 5:23",
        ]
    )
    lexer.input(snippet_str)
    token_assert_helper(lexer.token(), "SNIPPET_SPDX_ID", "SnippetSPDXID", 1)
    token_assert_helper(lexer.token(), "LINE", "SPDXRef-Snippet", 1)
    token_assert_helper(lexer.token(), "SNIPPET_LICENSE_COMMENT", "SnippetLicenseComments", 2)
    token_assert_helper(lexer.token(), "TEXT", "<text>Some lic comment.</text>", 2)
    token_assert_helper(lexer.token(), "SNIPPET_COPYRIGHT_TEXT", "SnippetCopyrightText", 3)
    token_assert_helper(lexer.token(), "TEXT", "<text> Copyright 2008-2010 John Smith </text>", 3)
    token_assert_helper(lexer.token(), "SNIPPET_COMMENT", "SnippetComment", 4)
    token_assert_helper(lexer.token(), "TEXT", "<text>Some snippet comment.</text>", 4)
    token_assert_helper(lexer.token(), "SNIPPET_NAME", "SnippetName", 5)
    token_assert_helper(lexer.token(), "LINE", "from linux kernel", 5)
    token_assert_helper(lexer.token(), "SNIPPET_FILE_SPDXID", "SnippetFromFileSPDXID", 6)
    token_assert_helper(lexer.token(), "LINE", "SPDXRef-DoapSource", 6)
    token_assert_helper(lexer.token(), "SNIPPET_LICENSE_CONCLUDED", "SnippetLicenseConcluded", 7)
    token_assert_helper(lexer.token(), "LINE", "Apache-2.0", 7)
    token_assert_helper(lexer.token(), "SNIPPET_LICENSE_INFO", "LicenseInfoInSnippet", 8)
    token_assert_helper(lexer.token(), "LINE", "Apache-2.0", 8)
    token_assert_helper(lexer.token(), "SNIPPET_BYTE_RANGE", "SnippetByteRange", 9)
    token_assert_helper(lexer.token(), "LINE", "310:420", 9)
    token_assert_helper(lexer.token(), "SNIPPET_LINE_RANGE", "SnippetLineRange", 10)
    token_assert_helper(lexer.token(), "LINE", "5:23", 10)


def test_tokenization_of_annotation(lexer):
    annotation_str = "\n".join(
        [
            "Annotator: Person: Jane Doe()",
            "AnnotationDate: 2010-01-29T18:30:22Z",
            "AnnotationComment: <text>Document level annotation</text>",
            "AnnotationType: OTHER",
            f"SPDXREF: {DOCUMENT_SPDX_ID}",
        ]
    )

    lexer.input(annotation_str)
    token_assert_helper(lexer.token(), "ANNOTATOR", "Annotator", 1)
    token_assert_helper(lexer.token(), "PERSON_VALUE", "Person: Jane Doe()", 1)
    token_assert_helper(lexer.token(), "ANNOTATION_DATE", "AnnotationDate", 2)
    token_assert_helper(lexer.token(), "ISO8601_DATE", "2010-01-29T18:30:22Z", 2)
    token_assert_helper(lexer.token(), "ANNOTATION_COMMENT", "AnnotationComment", 3)
    token_assert_helper(lexer.token(), "TEXT", "<text>Document level annotation</text>", 3)
    token_assert_helper(lexer.token(), "ANNOTATION_TYPE", "AnnotationType", 4)
    token_assert_helper(lexer.token(), "LINE", "OTHER", 4)
    token_assert_helper(lexer.token(), "ANNOTATION_SPDX_ID", "SPDXREF", 5)
    token_assert_helper(lexer.token(), "LINE", DOCUMENT_SPDX_ID, 5)


def test_tokenization_of_relationship(lexer):
    relationship_str = "\n".join(
        [
            f"Relationship: {DOCUMENT_SPDX_ID} DESCRIBES NONE",
            "RelationshipComment: This is a comment.",
            "Relationship: DocumentRef-extern:SPDXRef-Package DESCRIBES NONE",
        ]
    )

    lexer.input(relationship_str)
    token_assert_helper(lexer.token(), "RELATIONSHIP", "Relationship", 1)
    token_assert_helper(lexer.token(), "LINE", f"{DOCUMENT_SPDX_ID} DESCRIBES NONE", 1)
    token_assert_helper(lexer.token(), "RELATIONSHIP_COMMENT", "RelationshipComment", 2)
    token_assert_helper(lexer.token(), "LINE", "This is a comment.", 2)
    token_assert_helper(lexer.token(), "RELATIONSHIP", "Relationship", 3)
    token_assert_helper(lexer.token(), "LINE", "DocumentRef-extern:SPDXRef-Package DESCRIBES NONE", 3)
