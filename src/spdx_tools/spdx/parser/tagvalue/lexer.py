# Copyright (c) 2014 Ahmed H. Ismail
# Copyright (c) 2023 spdx contributors
# SPDX-License-Identifier: Apache-2.0
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ply import lex
from ply.lex import TOKEN


class SPDXLexer:
    reserved = {
        # Top level fields
        "SPDXVersion": "DOC_VERSION",
        "DataLicense": "DOC_LICENSE",
        "DocumentName": "DOC_NAME",
        "SPDXID": "SPDX_ID",
        "DocumentComment": "DOC_COMMENT",
        "DocumentNamespace": "DOC_NAMESPACE",
        "ExternalDocumentRef": "EXT_DOC_REF",
        # Creation info fields
        "Creator": "CREATOR",
        "Created": "CREATED",
        "CreatorComment": "CREATOR_COMMENT",
        "LicenseListVersion": "LICENSE_LIST_VERSION",
        # Annotation fields
        "Annotator": "ANNOTATOR",
        "AnnotationDate": "ANNOTATION_DATE",
        "AnnotationComment": "ANNOTATION_COMMENT",
        "AnnotationType": "ANNOTATION_TYPE",
        "SPDXREF": "ANNOTATION_SPDX_ID",
        # Relationship fields
        "Relationship": "RELATIONSHIP",
        "RelationshipComment": "RELATIONSHIP_COMMENT",
        # Package fields
        "PackageName": "PKG_NAME",
        "PackageVersion": "PKG_VERSION",
        "PackageDownloadLocation": "PKG_DOWNLOAD_LOCATION",
        "FilesAnalyzed": "PKG_FILES_ANALYZED",
        "PackageSummary": "PKG_SUMMARY",
        "PackageSourceInfo": "PKG_SOURCE_INFO",
        "PackageFileName": "PKG_FILE_NAME",
        "PackageSupplier": "PKG_SUPPLIER",
        "PackageOriginator": "PKG_ORIGINATOR",
        "PackageChecksum": "PKG_CHECKSUM",
        "PackageVerificationCode": "PKG_VERIFICATION_CODE",
        "PackageDescription": "PKG_DESCRIPTION",
        "PackageComment": "PKG_COMMENT",
        "PackageLicenseDeclared": "PKG_LICENSE_DECLARED",
        "PackageLicenseConcluded": "PKG_LICENSE_CONCLUDED",
        "PackageLicenseInfoFromFiles": "PKG_LICENSE_INFO",
        "PackageLicenseComments": "PKG_LICENSE_COMMENT",
        "PackageCopyrightText": "PKG_COPYRIGHT_TEXT",
        "PackageHomePage": "PKG_HOMEPAGE",
        "ExternalRef": "PKG_EXTERNAL_REF",
        "ExternalRefComment": "PKG_EXTERNAL_REF_COMMENT",
        "PackageAttributionText": "PKG_ATTRIBUTION_TEXT",
        "PrimaryPackagePurpose": "PRIMARY_PACKAGE_PURPOSE",
        "BuiltDate": "BUILT_DATE",
        "ReleaseDate": "RELEASE_DATE",
        "ValidUntilDate": "VALID_UNTIL_DATE",
        # File fields
        "FileName": "FILE_NAME",
        "FileType": "FILE_TYPE",
        "FileChecksum": "FILE_CHECKSUM",
        "LicenseConcluded": "FILE_LICENSE_CONCLUDED",
        "LicenseInfoInFile": "FILE_LICENSE_INFO",
        "FileCopyrightText": "FILE_COPYRIGHT_TEXT",
        "LicenseComments": "FILE_LICENSE_COMMENT",
        "FileComment": "FILE_COMMENT",
        "FileNotice": "FILE_NOTICE",
        "FileContributor": "FILE_CONTRIBUTOR",
        "FileAttributionText": "FILE_ATTRIBUTION_TEXT",
        # ExtractedLicensingInfo fields
        "LicenseID": "LICENSE_ID",
        "ExtractedText": "LICENSE_TEXT",
        "LicenseName": "LICENSE_NAME",
        "LicenseCrossReference": "LICENSE_CROSS_REF",
        "LicenseComment": "LICENSE_COMMENT",
        # Snippet fields
        "SnippetSPDXID": "SNIPPET_SPDX_ID",
        "SnippetName": "SNIPPET_NAME",
        "SnippetComment": "SNIPPET_COMMENT",
        "SnippetCopyrightText": "SNIPPET_COPYRIGHT_TEXT",
        "SnippetLicenseComments": "SNIPPET_LICENSE_COMMENT",
        "SnippetFromFileSPDXID": "SNIPPET_FILE_SPDXID",
        "SnippetLicenseConcluded": "SNIPPET_LICENSE_CONCLUDED",
        "LicenseInfoInSnippet": "SNIPPET_LICENSE_INFO",
        "SnippetAttributionText": "SNIPPET_ATTRIBUTION_TEXT",
        "SnippetByteRange": "SNIPPET_BYTE_RANGE",
        "SnippetLineRange": "SNIPPET_LINE_RANGE",
        # Common fields
        "NOASSERTION": "NO_ASSERTION",
        "NONE": "NONE",
    }
    states = (("text", "exclusive"),)

    tokens = [
        "TEXT",
        "TOOL_VALUE",
        "UNKNOWN_TAG",
        "ORGANIZATION_VALUE",
        "PERSON_VALUE",
        "ISO8601_DATE",
        "LINE",
        "CHECKSUM",
    ] + list(reserved.values())

    def __init__(self):
        self.lexer = None

    @TOKEN(r":\s*<text>")
    def t_text(self, t):
        t.lexer.text_start = t.lexer.lexpos - len("<text>")
        t.lexer.begin("text")

    @TOKEN(r"</text>\s*")
    def t_text_end(self, t):
        t.type = "TEXT"
        t.value = t.lexer.lexdata[t.lexer.text_start : t.lexer.lexpos]
        t.lexer.lineno += t.value.count("\n")
        t.value = t.value.strip()
        t.lexer.begin("INITIAL")
        return t

    @TOKEN(r".|\n")
    def t_text_any(self, t):
        pass

    def t_text_error(self, t):
        print("Lexer error in text state")

    @TOKEN(
        r":\s*(ADLER32|BLAKE2b-256|BLAKE2b-384|BLAKE2b-512|BLAKE3|MD2|MD4|MD5|MD6|SHA1|SHA224|SHA256|SHA384|SHA512|"
        r"SHA3-256|SHA3-384|SHA3-512):\s*([a-f0-9]*)"
    )
    def t_CHECKSUM(self, t):
        t.value = t.value[1:].strip()
        return t

    @TOKEN(r":\s*Tool:.+")
    def t_TOOL_VALUE(self, t):
        t.value = t.value[1:].strip()
        return t

    @TOKEN(r":\s*Organization:.+")
    def t_ORGANIZATION_VALUE(self, t):
        t.value = t.value[1:].strip()
        return t

    @TOKEN(r":\s*Person:.+")
    def t_PERSON_VALUE(self, t):
        t.value = t.value[1:].strip()
        return t

    @TOKEN(r":\s*\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\dZ")
    def t_ISO8601_DATE(self, t):
        t.value = t.value[1:].strip()
        return t

    @TOKEN(r"[a-zA-Z]+")
    def t_KEYWORD_AS_TAG(self, t):
        t.type = self.reserved.get(t.value, "UNKNOWN_TAG")
        t.value = t.value.strip()
        return t

    @TOKEN(r":.+")
    def t_LINE_OR_KEYWORD_VALUE(self, t):
        t.value = t.value[1:].strip()
        if t.value in self.reserved.keys():
            t.type = self.reserved[t.value]
        else:
            t.type = "LINE"
        return t

    @TOKEN(r"\#.*")
    def t_comment(self, t):
        pass

    @TOKEN(r"\n+")
    def t_newline(self, t):
        t.lexer.lineno += len(t.value)

    @TOKEN(r"[ \t]+")
    def t_whitespace(self, t):
        pass

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    def token(self):
        return self.lexer.token()

    def input(self, data):
        self.lexer.input(data)

    def t_error(self, t):
        t.lexer.skip(1)
        t.value = "Lexer error"
        return t
