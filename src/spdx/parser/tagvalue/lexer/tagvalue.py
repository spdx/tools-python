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

from ply import lex
from ply.lex import TOKEN


class SPDXLexer(object):
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
        "LicenseListVersion": "LIC_LIST_VER",
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
        "PackageDownloadLocation": "PKG_DOWN",
        "FilesAnalyzed": "PKG_FILES_ANALYZED",
        "PackageSummary": "PKG_SUM",
        "PackageSourceInfo": "PKG_SRC_INFO",
        "PackageFileName": "PKG_FILE_NAME",
        "PackageSupplier": "PKG_SUPPL",
        "PackageOriginator": "PKG_ORIG",
        "PackageChecksum": "PKG_CHECKSUM",
        "PackageVerificationCode": "PKG_VERF_CODE",
        "PackageDescription": "PKG_DESC",
        "PackageComment": "PKG_COMMENT",
        "PackageLicenseDeclared": "PKG_LICS_DECL",
        "PackageLicenseConcluded": "PKG_LICS_CONC",
        "PackageLicenseInfoFromFiles": "PKG_LICS_FFILE",
        "PackageLicenseComments": "PKG_LICS_COMMENT",
        "PackageCopyrightText": "PKG_CPY_TEXT",
        "PackageHomePage": "PKG_HOME",
        "ExternalRef": "PKG_EXT_REF",
        "ExternalRefComment": "PKG_EXT_REF_COMMENT",
        "PackageAttributionText": "PKG_ATTRIBUTION_TEXT",
        "PrimaryPackagePurpose": "PRIMARY_PACKAGE_PURPOSE",
        "BuiltDate": "BUILT_DATE",
        "ReleaseDate": "RELEASE_DATE",
        "ValidUntilDate": "VALID_UNTIL_DATE",
        # File fields
        "FileName": "FILE_NAME",
        "FileType": "FILE_TYPE",
        "FileChecksum": "FILE_CHECKSUM",
        "LicenseConcluded": "FILE_LICS_CONC",
        "LicenseInfoInFile": "FILE_LICS_INFO",
        "FileCopyrightText": "FILE_CR_TEXT",
        "LicenseComments": "FILE_LICS_COMMENT",
        "FileComment": "FILE_COMMENT",
        "FileNotice": "FILE_NOTICE",
        "FileContributor": "FILE_CONTRIB",
        "FileAttributionText": "FILE_ATTRIBUTION_TEXT",
        # ExtractedLicensingInfo fields
        "LicenseID": "LICS_ID",
        "ExtractedText": "LICS_TEXT",
        "LicenseName": "LICS_NAME",
        "LicenseCrossReference": "LICS_CRS_REF",
        "LicenseComment": "LICS_COMMENT",
        # Snippet fields
        "SnippetSPDXID": "SNIPPET_SPDX_ID",
        "SnippetName": "SNIPPET_NAME",
        "SnippetComment": "SNIPPET_COMMENT",
        "SnippetCopyrightText": "SNIPPET_CR_TEXT",
        "SnippetLicenseComments": "SNIPPET_LICS_COMMENT",
        "SnippetFromFileSPDXID": "SNIPPET_FILE_SPDXID",
        "SnippetLicenseConcluded": "SNIPPET_LICS_CONC",
        "LicenseInfoInSnippet": "SNIPPET_LICS_INFO",
        "SnippetAttributionText": "SNIPPET_ATTRIBUTION_TEXT",
        "SnippetByteRange": "SNIPPET_BYTE_RANGE",
        "SnippetLineRange": "SNIPPET_LINE_RANGE",
        # Common fields
        "NOASSERTION": "NO_ASSERTION",
        "NONE": "NONE",
        "SOURCE": "SOURCE",
        "BINARY": "BINARY",
        "ARCHIVE": "ARCHIVE",
        "APPLICATION": "APPLICATION",
        "AUDIO": "AUDIO",
        "IMAGE": "IMAGE",
        "TEXT": "FILETYPE_TEXT",
        "VIDEO": "VIDEO",
        "DOCUMENTATION": "DOCUMENTATION",
        "SPDX": "SPDX",
        "OTHER": "OTHER",
        "REVIEW": "REVIEW",
        "FRAMEWORK": "FRAMEWORK",
        "LIBRARY": "LIBRARY",
        "CONTAINER": "CONTAINER",
        "OPERATING-SYSTEM": "OPERATING_SYSTEM",
        "DEVICE": "DEVICE",
        "FIRMWARE": "FIRMWARE",
        "FILE": "FILE",
        "INSTALL": "INSTALL"
    }
    states = (("text", "exclusive"),)

    tokens = [
                 "TEXT",
                 "TOOL_VALUE",
                 "UNKNOWN_TAG",
                 "ORG_VALUE",
                 "PERSON_VALUE",
                 "DATE",
                 "LINE",
                 "CHECKSUM",
                 "DOC_REF_ID",
                 "DOC_URI",
                 "EXT_DOC_REF_CHECKSUM",
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
        t.value = t.lexer.lexdata[t.lexer.text_start: t.lexer.lexpos]
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
        r":\s*(ADLER32|BLAKE2b-256|BLAKE2b-384|BLAKE2b-512|BLAKE3|MD2|MD4|MD5|MD6|SHA1|SHA224|SHA256|SHA384|SHA512|SHA3-256|SHA3-384|SHA3-512):\s*([a-f0-9]*)")
    def t_CHECKSUM(self, t):
        t.value = t.value[1:].strip()
        return t

    @TOKEN(r":\s*DocumentRef-([A-Za-z0-9\+\.\-]+)")
    def t_DOC_REF_ID(self, t):
        t.value = t.value[1:].strip()
        return t

    @TOKEN(r"\s*((ht|f)tps?:\/\/\S*)")
    def t_DOC_URI(self, t):
        t.value = t.value.strip()
        return t

    @TOKEN(r"\s*SHA1:\s*[a-f0-9]{40}")
    def t_EXT_DOC_REF_CHECKSUM(self, t):
        t.value = t.value[1:].strip()
        return t

    @TOKEN(r":\s*Tool:.+")
    def t_TOOL_VALUE(self, t):
        t.value = t.value[1:].strip()
        return t

    @TOKEN(r":\s*Organization:.+")
    def t_ORG_VALUE(self, t):
        t.value = t.value[1:].strip()
        return t

    @TOKEN(r":\s*Person:.+")
    def t_PERSON_VALUE(self, t):
        t.value = t.value[1:].strip()
        return t

    @TOKEN(r":\s*\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\dZ")
    def t_DATE(self, t):
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
