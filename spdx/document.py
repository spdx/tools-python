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
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from spdx.file import File
from spdx.license import ExtractedLicense
from spdx.parsers.loggers import ErrorMessages

import warnings

from functools import total_ordering
from spdx.relationship import Relationship

from spdx.relationship import Relationship


@total_ordering
class ExternalDocumentRef(object):
    """
    External Document References entity that contains the following fields :
    - external_document_id: A unique string containing letters, numbers, '.',
        '-' or '+'.
    - spdx_document_uri: The unique ID of the SPDX document being referenced.
    - check_sum: The checksum of the referenced SPDX document.
    """

    def __init__(
        self, external_document_id=None, spdx_document_uri=None, checksum=None
    ):
        self.external_document_id = external_document_id
        self.spdx_document_uri = spdx_document_uri
        self.checksum = checksum

    def __eq__(self, other):
        return (
            isinstance(other, ExternalDocumentRef)
            and self.external_document_id == other.external_document_id
            and self.spdx_document_uri == other.spdx_document_uri
            and self.checksum == other.checksum
        )

    def __lt__(self, other):
        return (self.external_document_id, self.spdx_document_uri, self.checksum) < (
            other.external_document_id,
            other.spdx_document_uri,
            other.checksum,
        )

    def validate(self, messages: ErrorMessages) -> ErrorMessages:
        """
        Check that all the fields are valid.
        Appends any error messages to messages parameter shall be a ErrorMessages.
        """
        self.validate_ext_doc_id(messages)
        self.validate_spdx_doc_uri(messages)
        self.validate_checksum(messages)
        return messages

    def validate_ext_doc_id(self, messages):
        if not self.external_document_id:
            messages.append("ExternalDocumentRef has no External Document ID.")

    def validate_spdx_doc_uri(self, messages):
        if not self.spdx_document_uri:
            messages.append("ExternalDocumentRef has no SPDX Document URI.")

    def validate_checksum(self, messages):
        if not self.checksum:
            messages.append("ExternalDocumentRef has no Checksum.")


class Document(object):
    """
    Represent an SPDX document with these fields:
    - version: Spec version. Mandatory, one - Type: Version.
    - data_license: SPDX-Metadata license. Mandatory, one. Type: License.
    - name: Name of the document. Mandatory, one. Type: str.
    - spdx_id: SPDX Identifier for the document to refer to itself in
      relationship to other elements. Mandatory, one. Type: str.
    - ext_document_references: External SPDX documents referenced within the
        given SPDX document. Optional, one or many. Type: ExternalDocumentRef
    - comment: Comments on the SPDX file, optional one. Type: str
    - documentNamespace: SPDX document specific namespace. Mandatory, one. Type: str
    - creation_info: SPDX file creation info. Mandatory, one. Type: CreationInfo
    - package: Package described by this document. Mandatory, one. Type: Package
    - extracted_licenses: List of licenses extracted that are not part of the
      SPDX license list. Optional, many. Type: ExtractedLicense.
    - reviews: SPDX document review information, Optional zero or more.
      Type: Review.
    - annotations: SPDX document annotation information, Optional zero or more.
      Type: Annotation.
    - snippet: Snippet information. Optional zero or more. Type: Snippet.
    - relationships: Relationship between two SPDX elements. Optional zero or more.
      Type: Relationship. 
    """

    def __init__(
        self,
        version=None,
        data_license=None,
        name=None,
        spdx_id=None,
        namespace=None,
        comment=None,
        package=None,
        license_list_version=None,
    ):
        # avoid recursive import
        from spdx.creationinfo import CreationInfo

        self.version = version
        self.data_license = data_license
        self.name = name
        self.license_list_version=license_list_version
        self.spdx_id = spdx_id
        self.ext_document_references = []
        self.comment = comment
        self.namespace = namespace
        self.creation_info = CreationInfo()
        self.files: List['File'] = []
        self.packages = []
        if package is not None:
            self.packages.append(package)
        self.extracted_licenses = []
        self.reviews = []
        self.annotations = []
        self.relationships: List[Relationship] = []
        self.snippet = []

    def add_review(self, review):
        self.reviews.append(review)

    def add_annotation(self, annotation):
        self.annotations.append(annotation)

    def add_relationship(self, relationship):
        self.relationships.append(relationship)

    def add_extr_lic(self, lic):
        self.extracted_licenses.append(lic)

    def add_ext_document_reference(self, ext_doc_ref):
        self.ext_document_references.append(ext_doc_ref)

    def add_snippet(self, snip):
        self.snippet.append(snip)

    def add_package(self, package):
        self.packages.append(package)

    def add_file(self, file: 'File') -> None:
        self.files.append(file)

    # For backwards compatibility with older versions, we support a
    # mode where the first package in a document may be referred to as
    # the document's "package", and the files it contains may be
    # referred to as the document's files.  This usage is deprecated.

    @property
    def package(self):
        warnings.warn('document.package and document.files are deprecated; '
                      'use document.packages instead',
                      DeprecationWarning)
        if len(self.packages) == 0:
            return None
        else:
            return self.packages[0]

    @package.setter
    def package(self, value):
        warnings.warn('document.package and document.files are deprecated; '
                      'use document.packages instead',
                      DeprecationWarning)
        if len(self.packages) == 0:
            self.packages.append(value)
        else:
            self.packages[0] = value

    @property
    def has_comment(self):
        return self.comment is not None

    def validate(self, messages=None):
        """
        Validate all fields of the document and update the
        messages list with user friendly error messages for display.
        """
        if isinstance(messages, list):
            raise TypeError("messages should be None or an instance of ErrorMessages")
        if messages is None:
            messages = ErrorMessages()

        messages.push_context(self.name)
        self.validate_version(messages)
        self.validate_data_lics(messages)
        self.validate_name(messages)
        self.validate_spdx_id(messages)
        self.validate_namespace(messages)
        self.validate_ext_document_references(messages)
        self.validate_creation_info(messages)
        self.validate_files(messages)
        self.validate_packages(messages)
        self.validate_extracted_licenses(messages)
        self.validate_reviews(messages)
        self.validate_snippet(messages)
        self.validate_annotations(messages)
        self.validate_relationships(messages)
        messages.pop_context()
        return messages

    def validate_version(self, messages):
        if self.version is None:
            messages.append("Document has no version.")

    def validate_data_lics(self, messages):
        if self.data_license is None:
            messages.append("Document has no data license.")
        else:
            # FIXME: REALLY? what if someone wants to use something else?
            if self.data_license.identifier != "CC0-1.0":
                messages.append("Document data license must be CC0-1.0.")

    def validate_name(self, messages):
        if self.name is None:
            messages.append("Document has no name.")

    def validate_namespace(self, messages):
        if self.namespace is None:
            messages.append("Document has no namespace.")

    def validate_spdx_id(self, messages):
        if self.spdx_id is None:
            messages.append("Document has no SPDX Identifier.")
        else:
            if not self.spdx_id.endswith("SPDXRef-DOCUMENT"):
                messages.append("Invalid Document SPDX Identifier value.")

    def validate_ext_document_references(self, messages):
        for doc in self.ext_document_references:
            if isinstance(doc, ExternalDocumentRef):
                messages = doc.validate(messages)
            else:
                messages = list(messages) + [
                    "External document references must be of the type "
                    "spdx.document.ExternalDocumentRef and not " + str(type(doc))
                ]

    def validate_reviews(self, messages):
        for review in self.reviews:
            messages = review.validate(messages)

    def validate_files(self, messages: ErrorMessages) -> None:
        for file in self.files:
            messages = file.validate(messages)

    def validate_annotations(self, messages):
        for annotation in self.annotations:
            messages = annotation.validate(messages)

    def validate_relationships(self, messages):
        for relationship in self.relationships:
            messages = relationship.validate(messages)

    def validate_snippet(self, messages=None):
        for snippet in self.snippet:
            snippet.validate(messages)

    def validate_creation_info(self, messages):
        if self.creation_info is not None:
            self.creation_info.validate(messages)
        else:
            messages.append("Document has no creation information.")

    def validate_packages(self, messages):
        for package in self.packages:
            messages = package.validate(messages)

    def validate_extracted_licenses(self, messages):
        for lic in self.extracted_licenses:
            if isinstance(lic, ExtractedLicense):
                messages = lic.validate(messages)
            else:
                messages.append(
                    "Document extracted licenses must be of type "
                    "spdx.document.ExtractedLicense and not " + type(lic)
                )
