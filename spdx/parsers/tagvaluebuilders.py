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

import re
from typing import Dict, List

from spdx import annotation
from spdx import creationinfo
from spdx import file
from spdx import license
from spdx import package
from spdx import review
from spdx import snippet
from spdx import utils
from spdx import version
from spdx.checksum import Checksum
from spdx.document import ExternalDocumentRef, Document
from spdx.package import PackagePurpose
from spdx.parsers import validations
from spdx.parsers.builderexceptions import CardinalityError
from spdx.parsers.builderexceptions import OrderError
from spdx.parsers.builderexceptions import SPDXValueError
from spdx.relationship import Relationship


def str_from_text(text) -> str:
    """
    Return content of a free form text block as a string.
    """
    REGEX = re.compile("<text>((.|\n)+)</text>", re.UNICODE)
    match = REGEX.match(text)
    if match:
        return match.group(1)
    elif isinstance(text, str):
        return text
    else:
        return None


class DocBuilder(object):
    """
    Set the fields of the top level document model.
    """

    VERS_STR_REGEX = re.compile(r"SPDX-(\d+)\.(\d+)", re.UNICODE)

    def __init__(self):
        # FIXME: this state does not make sense
        self.reset_document()

    def set_doc_version(self, doc, value):
        """
        Set the document version.
        Raise SPDXValueError if malformed value.
        Raise CardinalityError if already defined.
        """
        if self.doc_version_set:
            raise CardinalityError("Document::Version")

        m = self.VERS_STR_REGEX.match(value)
        if m is None:
            raise SPDXValueError("Document::Version")

        self.doc_version_set = True
        doc.version = version.Version(
            major=int(m.group(1)), minor=int(m.group(2))
        )
        return True

    def set_doc_data_lics(self, doc, lics):
        """
        Set the document data license.
        Raise value error if malformed value
        Raise CardinalityError if already defined.
        """
        if self.doc_data_lics_set:
            raise CardinalityError("Document::DataLicense")

        if not validations.validate_data_lics(lics):
            raise SPDXValueError("Document::DataLicense")

        self.doc_data_lics_set = True
        doc.data_license = license.License.from_identifier(lics)
        return True

    def set_doc_name(self, doc, name):
        """
        Set the document name.
        Raise CardinalityError if already defined.
        """
        if self.doc_name_set:
            raise CardinalityError("Document::Name")

        self.doc_name_set = True
        doc.name = name
        return True

    def set_doc_spdx_id(self, doc, doc_spdx_id_line):
        """
        Set the document SPDX Identifier.
        Raise value error if malformed value.
        Raise CardinalityError if already defined.
        """
        if self.doc_spdx_id_set:
            raise CardinalityError("Document::SPDXID")

        if not doc_spdx_id_line == "SPDXRef-DOCUMENT":
            raise SPDXValueError("Document::SPDXID")

        doc.spdx_id = doc_spdx_id_line
        self.doc_spdx_id_set = True
        return True

    def set_doc_comment(self, doc, comment):
        """
        Set document comment.
        Raise CardinalityError if comment already set.
        Raise SPDXValueError if comment is not free form text or single line of text.
        """
        if self.doc_comment_set:
            raise CardinalityError("Document::Comment")

        if not validations.validate_doc_comment(comment):
            raise SPDXValueError("Document::Comment")

        self.doc_comment_set = True
        doc.comment = str_from_text(comment)
        return True

    def set_doc_namespace(self, doc, namespace):
        """
        Set the document namespace.
        Raise SPDXValueError if malformed value.
        Raise CardinalityError if already defined.
        """
        if self.doc_namespace_set:
            raise CardinalityError("Document::Namespace")

        if not validations.validate_doc_namespace(namespace):
            raise SPDXValueError("Document::Namespace")

        self.doc_namespace_set = True
        doc.namespace = namespace
        return True

    def reset_document(self):
        """
        Reset the state to allow building new documents
        """
        # FIXME: this state does not make sense
        self.doc_version_set = False
        self.doc_comment_set = False
        self.doc_namespace_set = False
        self.doc_data_lics_set = False
        self.doc_name_set = False
        self.doc_spdx_id_set = False


class ExternalDocumentRefBuilder(object):
    def set_ext_doc_id(self, doc, ext_doc_id):
        """
        Set the `external_document_id` attribute of the `ExternalDocumentRef` object.
        """
        doc.add_ext_document_reference(
            ExternalDocumentRef(external_document_id=ext_doc_id)
        )

    def set_spdx_doc_uri(self, doc, spdx_doc_uri):
        """
        Set the `spdx_document_uri` attribute of the `ExternalDocumentRef` object.
        """
        if not validations.validate_doc_namespace(spdx_doc_uri):
            raise SPDXValueError("Document::ExternalDocumentRef")

        doc.ext_document_references[-1].spdx_document_uri = spdx_doc_uri

    def set_chksum(self, doc, chksum):
        """
        Set the `check_sum` attribute of the `ExternalDocumentRef` object.
        """
        doc.ext_document_references[-1].checksum = Checksum.checksum_from_string(chksum)

    def add_ext_doc_refs(self, doc, ext_doc_id, spdx_doc_uri, chksum):
        self.set_ext_doc_id(doc, ext_doc_id)
        self.set_spdx_doc_uri(doc, spdx_doc_uri)
        self.set_chksum(doc, chksum)


class EntityBuilder(object):
    tool_re = re.compile(r"Tool:\s*(.+)", re.UNICODE)
    person_re = re.compile(r"Person:\s*(([^(])+)(\((.*)\))?", re.UNICODE)
    org_re = re.compile(r"Organization:\s*(([^(])+)(\((.*)\))?", re.UNICODE)
    PERSON_NAME_GROUP = 1
    PERSON_EMAIL_GROUP = 4
    ORG_NAME_GROUP = 1
    ORG_EMAIL_GROUP = 4
    TOOL_NAME_GROUP = 1

    def build_tool(self, doc, entity):
        """
        Build a tool object out of a string representation.
        Return built tool.
        Raise SPDXValueError if failed to extract tool name or name is malformed
        """
        match = self.tool_re.match(entity)
        if not match or not validations.validate_tool_name(match.group(self.TOOL_NAME_GROUP)):
            raise SPDXValueError("Failed to extract tool name")

        name = match.group(self.TOOL_NAME_GROUP)
        return creationinfo.Tool(name)

    def build_org(self, doc, entity):
        """
        Build an organization object of of a string representation.
        Return built organization.
        Raise SPDXValueError if failed to extract name.
        """
        match = self.org_re.match(entity)
        if not match or not validations.validate_org_name(match.group(self.ORG_NAME_GROUP)):
            raise SPDXValueError("Failed to extract Organization name")

        name = match.group(self.ORG_NAME_GROUP).strip()
        email = match.group(self.ORG_EMAIL_GROUP)
        if (email is not None) and (len(email) != 0):
            return creationinfo.Organization(name=name, email=email.strip())
        else:
            return creationinfo.Organization(name=name, email=None)

    def build_person(self, doc, entity):
        """
        Build an organization object of of a string representation.
        Return built organization. Raise SPDXValueError if failed to extract name.
        """
        match = self.person_re.match(entity)
        if not match or not validations.validate_person_name(match.group(self.PERSON_NAME_GROUP)):
            raise SPDXValueError("Failed to extract person name")

        name = match.group(self.PERSON_NAME_GROUP).strip()
        email = match.group(self.PERSON_EMAIL_GROUP)
        if (email is not None) and (len(email) != 0):
            return creationinfo.Person(name=name, email=email.strip())
        else:
            return creationinfo.Person(name=name, email=None)


class CreationInfoBuilder(object):
    def __init__(self):
        # FIXME: this state does not make sense
        self.reset_creation_info()

    def add_creator(self, doc, creator):
        """
        Add a creator to the document's creation info.
        Return true if creator is valid.
        Creator must be built by an EntityBuilder.
        Raise SPDXValueError if not a creator type.
        """
        if not validations.validate_creator(creator):
            raise SPDXValueError("CreationInfo::Creator")

        doc.creation_info.add_creator(creator)
        return True

    def set_created_date(self, doc, created):
        """
        Set created date.
        Raise CardinalityError if created date already set.
        Raise SPDXValueError if created is not a date.
        """
        if self.created_date_set:
            raise CardinalityError("CreationInfo::Created")

        date = utils.datetime_from_iso_format(created)
        if date is None:
            raise SPDXValueError("CreationInfo::Date")

        self.created_date_set = True
        doc.creation_info.created = date
        return True

    def set_creation_comment(self, doc, comment):
        """
        Set creation comment.
        Raise CardinalityError if comment already set.
        Raise SPDXValueError if not free form text or single line of text.
        """
        if self.creation_comment_set:
            raise CardinalityError("CreationInfo::Comment")

        if not validations.validate_creation_comment(comment):
            raise SPDXValueError("CreationInfo::Comment")

        self.creation_comment_set = True
        doc.creation_info.comment = str_from_text(comment)
        return True

    def set_lics_list_ver(self, doc, value):
        """
        Set the license list version.
        Raise CardinalityError if already set.
        Raise SPDXValueError if incorrect value.
        """
        if self.lics_list_ver_set:
            raise CardinalityError("CreationInfo::LicenseListVersion")

        vers = version.Version.from_str(value)
        if vers is None:
            raise SPDXValueError("CreationInfo::LicenseListVersion")

        self.lics_list_ver_set = True
        doc.creation_info.license_list_version = vers
        return True

    def reset_creation_info(self):
        """
        Reset builder state to allow building new creation info.
        """
        # FIXME: this state does not make sense
        self.created_date_set = False
        self.creation_comment_set = False
        self.lics_list_ver_set = False


class ReviewBuilder(object):
    def __init__(self):
        # FIXME: this state does not make sense
        self.reset_reviews()

    def reset_reviews(self):
        """
        Reset the builder's state to allow building new reviews.
        """
        # FIXME: this state does not make sense
        self.review_date_set = False
        self.review_comment_set = False

    def add_reviewer(self, doc, reviewer):
        """
        Adds a reviewer to the SPDX Document.
        Reviewer is an entity created by an EntityBuilder.
        Raise SPDXValueError if not a valid reviewer type.
        """
        # Each reviewer marks the start of a new review object.
        # FIXME: this state does not make sense
        self.reset_reviews()
        if not validations.validate_reviewer(reviewer):
            raise SPDXValueError("Review::Reviewer")

        doc.add_review(review.Review(reviewer=reviewer))
        return True

    def add_review_date(self, doc, reviewed):
        """
        Set the review date.
        Raise CardinalityError if already set.
        Raise OrderError if no reviewer defined before.
        Raise SPDXValueError if invalid reviewed value.
        """
        if len(doc.reviews) == 0:
            raise OrderError("Review::ReviewDate")

        if self.review_date_set:
            raise CardinalityError("Review::ReviewDate")

        date = utils.datetime_from_iso_format(reviewed)
        if date is None:
            raise SPDXValueError("Review::ReviewDate")

        self.review_date_set = True
        doc.reviews[-1].review_date = date
        return True

    def add_review_comment(self, doc, comment):
        """
        Set the review comment.
        Raise CardinalityError if already set.
        Raise OrderError if no reviewer defined before.
        Raise SPDXValueError if comment is not free form text or single line of text.
        """
        if len(doc.reviews) == 0:
            raise OrderError("ReviewComment")

        if self.review_comment_set:
            raise CardinalityError("ReviewComment")

        if not validations.validate_review_comment(comment):
            raise SPDXValueError("ReviewComment::Comment")

        self.review_comment_set = True
        doc.reviews[-1].comment = str_from_text(comment)
        return True


class AnnotationBuilder(object):
    def __init__(self):
        # FIXME: this state does not make sense
        self.reset_annotations()

    def reset_annotations(self):
        """
        Reset the builder's state to allow building new annotations.
        """
        # FIXME: this state does not make sense
        self.annotation_date_set = False
        self.annotation_comment_set = False
        self.annotation_type_set = False
        self.annotation_spdx_id_set = False

    def add_annotator(self, doc, annotator):
        """
        Add an annotator to the SPDX Document.
        Annotator is an entity created by an EntityBuilder.
        Raise SPDXValueError if not a valid annotator type.
        """
        # Each annotator marks the start of a new annotation object.
        # FIXME: this state does not make sense
        self.reset_annotations()
        if not validations.validate_annotator(annotator):
            raise SPDXValueError("Annotation::Annotator")

        doc.add_annotation(annotation.Annotation(annotator=annotator))
        return True

    def add_annotation_date(self, doc, annotation_date):
        """
        Set the annotation date.
        Raise CardinalityError if already set.
        Raise OrderError if no annotator defined before.
        Raise SPDXValueError if invalid value.
        """
        if len(doc.annotations) == 0:
            raise OrderError("Annotation::AnnotationDate")

        if self.annotation_date_set:
            raise CardinalityError("Annotation::AnnotationDate")

        date = utils.datetime_from_iso_format(annotation_date)
        if date is None:
            raise SPDXValueError("Annotation::AnnotationDate")

        self.annotation_date_set = True
        doc.annotations[-1].annotation_date = date
        return True

    def add_annotation_comment(self, doc, comment):
        """
        Set the annotation comment.
        Raise CardinalityError if already set.
        Raise OrderError if no annotator defined before.
        Raise SPDXValueError if comment is not free form text or single line of text.
        """
        if len(doc.annotations) == 0:
            raise OrderError("AnnotationComment::Comment")

        if self.annotation_comment_set:
            raise CardinalityError("AnnotationComment::Comment")

        if not validations.validate_annotation_comment(comment):
            raise SPDXValueError("AnnotationComment::Comment")

        self.annotation_comment_set = True
        doc.annotations[-1].comment = str_from_text(comment)
        return True

    def add_annotation_type(self, doc, annotation_type):
        """
        Set the annotation type.
        Raise CardinalityError if already set.
        Raise OrderError if no annotator defined before.
        Raise SPDXValueError if invalid value.
        """
        if len(doc.annotations) == 0:
            raise OrderError("Annotation::AnnotationType")

        if self.annotation_type_set:
            raise CardinalityError("Annotation::AnnotationType")

        if not validations.validate_annotation_type(annotation_type):
            raise SPDXValueError("Annotation::AnnotationType")

        self.annotation_type_set = True
        doc.annotations[-1].annotation_type = annotation_type
        return True

    def set_annotation_spdx_id(self, doc, spdx_id):
        """
        Set the annotation SPDX Identifier.
        Raise CardinalityError if already set.
        Raise OrderError if no annotator defined before.
        """
        if len(doc.annotations) == 0:
            raise OrderError("Annotation::SPDXREF")

        if self.annotation_spdx_id_set:
            raise CardinalityError("Annotation::SPDXREF")

        self.annotation_spdx_id_set = True
        doc.annotations[-1].spdx_id = spdx_id
        return True


class RelationshipBuilder(object):
    def __init__(self):
        # FIXME: this state does not make sense
        self.reset_relationship()

    def reset_relationship(self):
        """
        Reset the builder's state to allow building new relationships.
        """
        # FIXME: this state does not make sense
        self.relationship_comment_set = False

    def add_relationship(self, doc: Document, relationship_term: str) -> bool:
        """
        Raise SPDXValueError if type is unknown.
        """
        self.reset_relationship()
        relationship_to_add = Relationship(relationship_term)
        existing_relationships: List[Relationship] = doc.relationships

        if relationship_to_add not in existing_relationships:
            doc.add_relationship(relationship_to_add)
            return True

        existing_relationship: Relationship = existing_relationships[existing_relationships.index(relationship_to_add)]

        # If the relationship already exists without comment, we remove the old one and re-append it at the end. This
        # allows to add a comment to the relationship (since a comment will always be added to the latest
        # relationship). If an equal relationship with comment already exists, we ignore the new relationship.
        if not existing_relationship.has_comment:
            existing_relationships.remove(relationship_to_add)
            doc.add_relationship(relationship_to_add)
            return True

        return False

    def add_relationship_comment(self, doc: Document, comment: str) -> bool:
        """
        Set the annotation comment.
        Raise CardinalityError if already set.
        Raise OrderError if no relationship defined before it.
        Raise SPDXValueError if comment is not free form text or single line of text.
        """
        if len(doc.relationships) == 0:
            raise OrderError("RelationshipComment::Comment")

        if self.relationship_comment_set:
            raise CardinalityError("RelationshipComment::Comment")

        if not validations.validate_relationship_comment(comment):
            raise SPDXValueError("RelationshipComment::Comment")

        self.relationship_comment_set = True
        doc.relationships[-1].comment = str_from_text(comment)
        return True


class PackageBuilder(object):
    VERIF_CODE_REGEX = re.compile(r"([0-9a-f]+)\s*(\(\s*(.+)\))?", re.UNICODE)
    VERIF_CODE_CODE_GRP = 1
    VERIF_CODE_EXC_FILES_GRP = 3

    def __init__(self):
        # FIXME: this state does not make sense
        self.reset_package()

    def reset_package(self):
        """Resets the builder's state in order to build new packages."""
        # FIXME: this state does not make sense
        self.package_set = False
        self.package_spdx_id_set = False
        self.package_vers_set = False
        self.package_file_name_set = False
        self.package_supplier_set = False
        self.package_originator_set = False
        self.package_down_location_set = False
        self.package_files_analyzed_set = False
        self.package_home_set = False
        self.package_verif_set = False
        self.package_chk_sum_set = False
        self.package_source_info_set = False
        self.package_conc_lics_set = False
        self.package_license_declared_set = False
        self.package_license_comment_set = False
        self.package_cr_text_set = False
        self.package_summary_set = False
        self.package_desc_set = False
        self.package_comment_set = False
        self.package_primary_purpose_set = False
        self.package_built_date_set = False
        self.package_release_date_set = False
        self.package_valid_until_date_set = False
        # self.package_attribution_text_set = False
        self.pkg_ext_comment_set = False

    def create_package(self, doc, name):
        """
        Create a package for the SPDX Document.
        name - any string.
        Raise CardinalityError if package already defined.
        """
        self.reset_package()
        self.package_set = True
        doc.add_package(package.Package(name=name))
        return True

    def set_pkg_spdx_id(self, doc, spdx_id):
        """
        Set the Package SPDX Identifier.
        Raise SPDXValueError if malformed value.
        Raise CardinalityError if already defined.
        """
        self.assert_package_exists()
        if self.package_spdx_id_set:
            raise CardinalityError("Package::SPDXID")

        if not validations.validate_pkg_spdx_id(spdx_id):
            raise SPDXValueError("Package::SPDXID")

        self.package_spdx_id_set = True
        doc.packages[-1].spdx_id = spdx_id
        return True

    def set_pkg_vers(self, doc, version):
        """
        Set package version, if not already set.
        version - Any string.
        Raise CardinalityError if already has a version.
        Raise OrderError if no package previously defined.
        """
        self.assert_package_exists()
        if self.package_vers_set:
            raise CardinalityError("Package::Version")

        self.package_vers_set = True
        doc.packages[-1].version = version
        return True

    def set_pkg_file_name(self, doc, name):
        """
        Set the package file name, if not already set.
        name - Any string.
        Raise CardinalityError if already has a file_name.
        Raise OrderError if no package previously defined.
        """
        self.assert_package_exists()
        if self.package_file_name_set:
            raise CardinalityError("Package::FileName")

        self.package_file_name_set = True
        doc.packages[-1].file_name = name
        return True

    def set_pkg_supplier(self, doc, entity):
        """
        Set the package supplier, if not already set.
        entity - Organization, Person or NoAssert.
        Raise CardinalityError if already has a supplier.
        Raise OrderError if no package previously defined.
        """
        self.assert_package_exists()
        if self.package_supplier_set:
            raise CardinalityError("Package::Supplier")

        if not validations.validate_pkg_supplier(entity):
            raise SPDXValueError("Package::Supplier")

        self.package_supplier_set = True
        doc.packages[-1].supplier = entity
        return True

    def set_pkg_originator(self, doc, entity):
        """
        Set the package originator, if not already set.
        entity - Organization, Person or NoAssert.
        Raise CardinalityError if already has an originator.
        Raise OrderError if no package previously defined.
        """
        self.assert_package_exists()
        if self.package_originator_set:
            raise CardinalityError("Package::Originator")

        if not validations.validate_pkg_originator(entity):
            raise SPDXValueError("Package::Originator")

        self.package_originator_set = True
        doc.packages[-1].originator = entity
        return True

    def set_pkg_down_location(self, doc, location):
        """
        Set the package download location, if not already set.
        location - A string
        Raise CardinalityError if already defined.
        Raise OrderError if no package previously defined.
        """
        self.assert_package_exists()
        if self.package_down_location_set:
            raise CardinalityError("Package::DownloadLocation")

        self.package_down_location_set = True
        doc.packages[-1].download_location = location
        return True

    def set_pkg_files_analyzed(self, doc, files_analyzed):
        """
        Set the package files analyzed, if not already set.
        Raise SPDXValueError if malformed value, CardinalityError if
        already defined.
        """
        self.assert_package_exists()
        if self.package_files_analyzed_set:
            raise CardinalityError("Package::FilesAnalyzed")

        if files_analyzed is None:
            return True

        if not validations.validate_pkg_files_analyzed(files_analyzed):
            raise SPDXValueError("Package::FilesAnalyzed")

        self.package_files_analyzed_set = True
        if isinstance(files_analyzed, str):
            files_analyzed = files_analyzed.lower() == "true"
        doc.packages[-1].files_analyzed = files_analyzed
        # convert to boolean;
        # validate_pkg_files_analyzed already checked if
        # files_analyzed is in ['True', 'true', 'False', 'false']
        return True

    def set_pkg_home(self, doc, location):
        """Set the package homepage location if not already set.
        location - A string or None or NoAssert.
        Raise CardinalityError if already defined.
        Raise OrderError if no package previously defined.
        Raise SPDXValueError if location has incorrect value.
        """
        self.assert_package_exists()
        if self.package_home_set:
            raise CardinalityError("Package::HomePage")

        if not validations.validate_pkg_homepage(location):
            raise SPDXValueError("Package::HomePage")

        self.package_home_set = True
        doc.packages[-1].homepage = location
        return True

    def set_pkg_verif_code(self, doc, code):
        """
        Set the package verification code, if not already set.
        code - A string.
        Raise CardinalityError if already defined.
        Raise OrderError if no package previously defined.
        Raise Value error if doesn't match verifcode form
        """
        self.assert_package_exists()
        if self.package_verif_set:
            raise CardinalityError("Package::VerificationCode")

        match = self.VERIF_CODE_REGEX.match(code)
        if not match:
            raise SPDXValueError("Package::VerificationCode")

        self.package_verif_set = True
        doc.packages[-1].verif_code = match.group(self.VERIF_CODE_CODE_GRP)

        if match.group(self.VERIF_CODE_EXC_FILES_GRP) is not None:
            doc.packages[-1].verif_exc_files = match.group(
                self.VERIF_CODE_EXC_FILES_GRP
            ).split(",")
        return True

    def set_pkg_checksum(self, doc, checksum):
        """
        Set the package checksum, if not already set.
        checksum - A string
        Raise OrderError if no package previously defined.
        """
        self.assert_package_exists()
        self.package_chk_sum_set = True
        doc.packages[-1].set_checksum(Checksum.checksum_from_string(checksum))
        return True

    def set_pkg_source_info(self, doc, text):
        """
        Set the package's source information, if not already set.
        text - Free form text.
        Raise CardinalityError if already defined.
        Raise OrderError if no package previously defined.
        SPDXValueError if text is not free form text or single line of text.
        """
        self.assert_package_exists()
        if self.package_source_info_set:
            raise CardinalityError("Package::SourceInfo")

        if not validations.validate_pkg_src_info(text):
            raise SPDXValueError("Package::SourceInfo")

        self.package_source_info_set = True
        doc.packages[-1].source_info = str_from_text(text)
        return True

    def set_pkg_licenses_concluded(self, doc, licenses):
        """
        Set the package's concluded licenses.
        licenses - License info.
        Raise CardinalityError if already defined.
        Raise OrderError if no package previously defined.
        Raise SPDXValueError if data malformed.
        """
        self.assert_package_exists()
        if self.package_conc_lics_set:
            raise CardinalityError("Package::ConcludedLicenses")

        if not validations.validate_lics_conc(licenses, optional=True):
            raise SPDXValueError("Package::ConcludedLicenses")

        self.package_conc_lics_set = True
        doc.packages[-1].conc_lics = licenses
        return True

    def set_pkg_license_from_file(self, doc, lic):
        """
        Add a license from a file to the package.
        Raise SPDXValueError if data malformed.
        Raise OrderError if no package previously defined.
        """
        self.assert_package_exists()
        if not validations.validate_lics_from_file(lic, optional=True):
            raise SPDXValueError("Package::LicensesFromFile")

        doc.packages[-1].licenses_from_files.append(lic)
        return True

    def set_pkg_license_declared(self, doc, lic):
        """
        Set the package's declared license.
        Raise SPDXValueError if data malformed.
        Raise OrderError if no package previously defined.
        Raise CardinalityError if already set.
        """
        self.assert_package_exists()
        if self.package_license_declared_set:
            raise CardinalityError("Package::LicenseDeclared")

        if not validations.validate_lics_conc(lic, optional=True):
            raise SPDXValueError("Package::LicenseDeclared")

        self.package_license_declared_set = True
        doc.packages[-1].license_declared = lic
        return True

    def set_pkg_license_comment(self, doc, text):
        """
        Set the package's license comment.
        Raise OrderError if no package previously defined.
        Raise CardinalityError if already set.
        Raise SPDXValueError if text is not free form text or single line of text.
        """
        self.assert_package_exists()
        if self.package_license_comment_set:
            raise CardinalityError("Package::LicenseComment")

        if not validations.validate_pkg_lics_comment(text):
            raise SPDXValueError("Package::LicenseComment")

        self.package_license_comment_set = True
        doc.packages[-1].license_comment = str_from_text(text)
        return True

    def set_pkg_attribution_text(self, doc, text):
        """
        Set the package's attribution text .
        Raise SPDXValueError if text is not free form text or single line of text.
        """
        self.assert_package_exists()
        if not validations.validate_pkg_attribution_text(text):
            raise SPDXValueError("Package::AttributionText")

        doc.packages[-1].attribution_text = str_from_text(text)
        return True

    def set_pkg_cr_text(self, doc, text):
        """
        Set the package's copyright text.
        Raise OrderError if no package previously defined.
        Raise CardinalityError if already set.
        Raise value error if text is not one of [None, NOASSERT, TEXT] or single line of text.
        """
        self.assert_package_exists()
        if self.package_cr_text_set:
            raise CardinalityError("Package::CopyrightText")

        if not validations.validate_pkg_cr_text(text, optional=True):
            raise SPDXValueError("Package::CopyrightText")

        self.package_cr_text_set = True
        if isinstance(text, str):
            doc.packages[-1].cr_text = str_from_text(text)
        else:
            doc.packages[-1].cr_text = text  # None or NoAssert

    def set_pkg_summary(self, doc, text):
        """
        Set the package summary.
        Raise SPDXValueError if text is not free form text or single line of text.
        Raise CardinalityError if summary already set.
        Raise OrderError if no package previously defined.
        """
        self.assert_package_exists()
        if self.package_summary_set:
            raise CardinalityError("Package::Summary")

        if not validations.validate_pkg_summary(text):
            raise SPDXValueError("Package::Summary")

        self.package_summary_set = True
        doc.packages[-1].summary = str_from_text(text)

    def set_pkg_desc(self, doc, text):
        """
        Set the package's description.
        Raise SPDXValueError if text is not free form text or single line of text.
        Raise CardinalityError if description already set.
        Raise OrderError if no package previously defined.
        """
        self.assert_package_exists()
        if self.package_desc_set:
            raise CardinalityError("Package::Description")

        if not validations.validate_pkg_desc(text):
            raise SPDXValueError("Package::Description")

        self.package_desc_set = True
        doc.packages[-1].description = str_from_text(text)

    def set_pkg_comment(self, doc, text):
        """
        Set the package's comment.
        Raise SPDXValueError if text is not free form text or single line of text.
        Raise CardinalityError if comment already set.
        Raise OrderError if no package previously defined.
        """
        self.assert_package_exists()
        if self.package_comment_set:
            raise CardinalityError("Package::Comment")

        if not validations.validate_pkg_comment(text):
            raise SPDXValueError("Package::Comment")

        self.package_comment_set = True
        doc.packages[-1].comment = str_from_text(text)

    def set_pkg_primary_package_purpose(self, doc, purpose):
        """
        Set the package's primary purpose.
        Raise CardinalityError if more than one purpose is set.
        Raise SPDXValueError if purpose is unknown.
        """
        self.assert_package_exists()
        if self.package_primary_purpose_set:
            raise CardinalityError("Package::PrimaryPackagePurpose")

        self.package_primary_purpose_set = True
        purpose = purpose.replace("-", "_")
        for purpose_enum in PackagePurpose:
            if purpose == purpose_enum.name:
                doc.packages[-1].primary_package_purpose = purpose_enum
                return True
        else:
            raise SPDXValueError("Package::PrimaryPackagePurpose")

    def set_pkg_built_date(self, doc, built_date):
        """
        Set the package`s built date.
        Raise CardinalityError if built_date date already set.
        Raise SPDXValueError if built_date is not a date.
        """
        self.assert_package_exists()
        if self.package_built_date_set:
            raise CardinalityError("Package::BuiltDate")

        date = utils.datetime_from_iso_format(built_date)
        if date is None:
            raise SPDXValueError("Package::BuiltDate")

        self.package_built_date_set = True
        doc.packages[-1].built_date = date
        return True

    def set_pkg_release_date(self, doc, release_date):
        """
        Set the package`s release date.
        Raise CardinalityError if release_date date already set.
        Raise SPDXValueError if release_date is not a date.
        """
        self.assert_package_exists()
        if self.package_release_date_set:
            raise CardinalityError("Package::ReleaseDate")

        date = utils.datetime_from_iso_format(release_date)
        if date is None:
            raise SPDXValueError("Package::ReleaseDate")

        self.package_release_date_set = True
        doc.packages[-1].release_date = date
        return True

    def set_pkg_valid_until_date(self, doc, valid_until_date):
        """
        Set the package`s valid_until date.
        Raise CardinalityError if valid_until_date date already set.
        Raise SPDXValueError if valid_until_date is not a date.
        """
        self.assert_package_exists()
        if self.package_valid_until_date_set:
            raise CardinalityError("Package::ValidUntilDate")

        date = utils.datetime_from_iso_format(valid_until_date)
        if date is None:
            raise SPDXValueError("Package::ValidUntilDate")

        self.package_valid_until_date_set = True
        doc.packages[-1].valid_until_date = date
        return True

    def set_pkg_ext_ref_category(self, doc, category):
        """
        Set the `category` attribute of the `ExternalPackageRef` object.
        """
        self.assert_package_exists()
        if not validations.validate_pkg_ext_ref_category(category):
            raise SPDXValueError("ExternalRef::Category")

        if (
            len(doc.packages[-1].pkg_ext_refs)
            and doc.packages[-1].pkg_ext_refs[-1].category is None
        ):
            doc.packages[-1].pkg_ext_refs[-1].category = category
        else:
            doc.packages[-1].add_pkg_ext_refs(
                package.ExternalPackageRef(category=category)
            )

    def set_pkg_ext_ref_type(self, doc, pkg_ext_ref_type):
        """
        Set the `pkg_ext_ref_type` attribute of the `ExternalPackageRef` object.
        """
        self.assert_package_exists()
        if not validations.validate_pkg_ext_ref_type(pkg_ext_ref_type):
            raise SPDXValueError("ExternalRef::Type")

        if (
            len(doc.packages[-1].pkg_ext_refs)
            and doc.packages[-1].pkg_ext_refs[-1].pkg_ext_ref_type is None
        ):
            doc.packages[-1].pkg_ext_refs[-1].pkg_ext_ref_type = pkg_ext_ref_type
        else:
            doc.packages[-1].add_pkg_ext_refs(
                package.ExternalPackageRef(pkg_ext_ref_type=pkg_ext_ref_type)
            )

    def set_pkg_ext_ref_locator(self, doc, locator):
        """
        Set the `locator` attribute of the `ExternalPackageRef` object.
        """
        self.assert_package_exists()
        if (
            len(doc.packages[-1].pkg_ext_refs)
            and doc.packages[-1].pkg_ext_refs[-1].locator is None
        ):
            doc.packages[-1].pkg_ext_refs[-1].locator = locator
        else:
            doc.packages[-1].add_pkg_ext_refs(package.ExternalPackageRef(locator=locator))

    def add_pkg_ext_ref_comment(self, doc, comment):
        """
        Set the `comment` attribute of the `ExternalPackageRef` object.
        """
        self.assert_package_exists()
        if not len(doc.packages[-1].pkg_ext_refs):
            raise OrderError("Package::ExternalRef")

        if not validations.validate_pkg_ext_ref_comment(comment):
            raise SPDXValueError("ExternalRef::Comment")

        doc.packages[-1].pkg_ext_refs[-1].comment = str_from_text(comment)

    def add_pkg_ext_refs(self, doc, category, pkg_ext_ref_type, locator):
        self.set_pkg_ext_ref_category(doc, category)
        self.set_pkg_ext_ref_type(doc, pkg_ext_ref_type)
        self.set_pkg_ext_ref_locator(doc, locator)

    def assert_package_exists(self):
        if not self.package_set:
            raise OrderError("Package")


class FileBuilder(object):
    def __init__(self):
        # FIXME: this state does not make sense
        self.reset_file_stat()

    def set_file_name(self, doc, name):
        doc.files.append(file.File(name))
        # A file name marks the start of a new file instance.
        # The builder must be reset
        # FIXME: this state does not make sense
        self.reset_file_stat()
        return True

    def set_file_spdx_id(self, doc, spdx_id):
        """
        Set the file SPDX Identifier.
        Raise OrderError if no package or no file defined.
        Raise SPDXValueError if malformed value.
        Raise CardinalityError if more than one spdx_id set.
        """
        if not self.has_file(doc):
            raise OrderError("File::SPDXID")

        if self.file_spdx_id_set:
            raise CardinalityError("File::SPDXID")

        if not validations.validate_file_spdx_id(spdx_id):
            raise SPDXValueError("File::SPDXID")

        self.file_spdx_id_set = True
        self.file(doc).spdx_id = spdx_id
        return True

    def set_file_comment(self, doc, text):
        """
        Raise OrderError if no package or no file defined.
        Raise CardinalityError if more than one comment set.
        Raise SPDXValueError if text is not free form text or single line of text.
        """
        if not self.has_file(doc):
            raise OrderError("File::Comment")

        if self.file_comment_set:
            raise CardinalityError("File::Comment")

        if not validations.validate_file_comment(text):
            raise SPDXValueError("File::Comment")

        self.file_comment_set = True
        self.file(doc).comment = str_from_text(text)
        return True

    def set_file_attribution_text(self, doc, text):
        """
        Set the file's attribution text .
        Raise OrderError if no package or no file defined.
        Raise SPDXValueError if text is not free form text or single line of text.
        """
        if not self.has_file(doc):
            raise OrderError("File::AttributionText")

        if not validations.validate_file_attribution_text(text):
            raise SPDXValueError("File::AttributionText")

        self.file(doc).attribution_text = str_from_text(text)
        return True

    def set_file_type(self, doc, type_value):
        """
        Raise OrderError if no package or file defined.
        Raise CardinalityError if more than one type set.
        Raise SPDXValueError if type is unknown.
        """
        if not self.has_file(doc):
            raise OrderError("File::FileType")

        if type_value not in file.FileType.__members__:
            raise SPDXValueError("File:FileType")

        file_type = file.FileType[type_value]

        spdx_file = self.file(doc)
        if file_type in spdx_file.file_types:
            raise CardinalityError("File::FileType")

        spdx_file.file_types.append(file_type)

    def set_file_checksum(self, doc: Document, checksum: str):
        """
        Raise OrderError if no file defined.
        """
        if self.has_file(doc):
            new_checksum = Checksum.checksum_from_string(checksum)
            self.file(doc).set_checksum(new_checksum)
        else:
            raise OrderError("File::CheckSum")
        return True

    def set_concluded_license(self, doc, lic):
        """
        Raise OrderError if no package or file defined.
        Raise CardinalityError if already set.
        Raise SPDXValueError if malformed.
        """
        if not self.has_file(doc):
            raise OrderError("File::ConcludedLicense")

        if self.file_conc_lics_set:
            raise CardinalityError("File::ConcludedLicense")

        if not validations.validate_lics_conc(lic, optional=True):
            raise SPDXValueError("File::ConcludedLicense")

        self.file_conc_lics_set = True
        self.file(doc).conc_lics = lic
        return True

    def set_file_license_in_file(self, doc, lic):
        """
        Raise OrderError if no package or file defined.
        Raise SPDXValueError if malformed value.
        """
        if not self.has_file(doc):
            raise OrderError("File::LicenseInFile")

        if not validations.validate_file_lics_in_file(lic):
            raise SPDXValueError("File::LicenseInFile")

        self.file(doc).add_lics(lic)
        return True

    def set_file_license_comment(self, doc, text):
        """
        Raise OrderError if no package or file defined.
        Raise SPDXValueError if text is not free form text or single line of text.
        Raise CardinalityError if more than one per file.
        """
        if not self.has_file(doc):
            raise OrderError("File::LicenseComment")

        if self.file_license_comment_set:
            raise CardinalityError("File::LicenseComment")

        if not validations.validate_file_lics_comment(text):
            raise SPDXValueError("File::LicenseComment")

        self.file_license_comment_set = True
        self.file(doc).license_comment = str_from_text(text)

    def set_file_copyright(self, doc, text):
        """
        Raise OrderError if no package or file defined.
        Raise SPDXValueError if not free form text or NONE or NO_ASSERT or single line of text.
        Raise CardinalityError if more than one.
        """
        if not self.has_file(doc):
            raise OrderError("File::CopyRight")

        if self.file_copytext_set:
            raise CardinalityError("File::CopyRight")

        if not validations.validate_file_cpyright(text, optional=True):
            raise SPDXValueError("File::CopyRight")

        self.file_copytext_set = True
        if isinstance(text, str):
            self.file(doc).copyright = str_from_text(text)
        else:
            self.file(doc).copyright = text  # None or NoAssert
        return True

    def set_file_notice(self, doc, text):
        """
        Raise OrderError if no package or file defined.
        Raise SPDXValueError if not free form text or single line of text.
        Raise CardinalityError if more than one.
        """
        if not self.has_file(doc):
            raise OrderError("File::Notice")

        if self.file_notice_set:
            raise CardinalityError("File::Notice")

        if not validations.validate_file_notice(text):
            raise SPDXValueError("File::Notice")

        self.file_notice_set = True
        self.file(doc).notice = str_from_text(text)

    def add_file_contribution(self, doc, value):
        """
        Raise OrderError if no package or file defined.
        """
        if not self.has_file(doc):
            raise OrderError("File::Contributor")

        self.file(doc).add_contrib(value)

    def add_file_dep(self, doc, value):
        """
        Raise OrderError if no package or file defined.
        """
        if not self.has_file(doc):
            raise OrderError("File::Dependency")

        self.file(doc).add_depend(value)

    def set_file_atrificat_of_project(self, doc, symbol, value):
        """
        Set a file name, uri or home artifact.
        Raise OrderError if no package or file defined.
        """
        if not self.has_file(doc):
            raise OrderError("File::Artifact")

        self.file(doc).add_artifact(symbol, value)

    def file(self, doc):
        """
        Return the last file in the document's file list.
        """
        return doc.files[-1]

    def has_file(self, doc):
        """
        Return true if the document has at least one file.
        """
        return len(doc.files) != 0

    def has_package(self, doc):
        """
        Return true if the document has a package.
        """
        return len(doc.packages) != 0

    def reset_file_stat(self):
        """
        Reset the builder's state to enable building new files.
        """
        # FIXME: this state does not make sense
        self.file_spdx_id_set = False
        self.file_comment_set = False
        self.file_type_set = False
        self.file_chksum_set = False
        self.file_conc_lics_set = False
        self.file_license_comment_set = False
        self.file_notice_set = False
        self.file_copytext_set = False


class LicenseBuilder(object):
    def __init__(self):
        # FIXME: this state does not make sense
        self.reset_extr_lics()

    def extr_lic(self, doc):
        """
        Retrieve last license in extracted license list.
        """
        return doc.extracted_licenses[-1]

    def has_extr_lic(self, doc):
        return len(doc.extracted_licenses) != 0

    def set_lic_id(self, doc, lic_id):
        """
        Add a new extracted license to the document.
        Raise SPDXValueError if data format is incorrect.
        """
        # FIXME: this state does not make sense
        self.reset_extr_lics()
        if not validations.validate_extracted_lic_id(lic_id):
            raise SPDXValueError("ExtractedLicense::id")

        doc.add_extr_lic(license.ExtractedLicense(lic_id))
        return True

    def set_lic_text(self, doc, text):
        """
        Set license extracted text.
        Raise SPDXValueError if text is not free form text or single line of text.
        Raise OrderError if no license ID defined.
        """
        if not self.has_extr_lic(doc):
            raise OrderError("ExtractedLicense::text")

        if self.extr_text_set:
            raise CardinalityError("ExtractedLicense::text")

        if not validations.validate_is_free_form_text_or_str(text):
            raise SPDXValueError("ExtractedLicense::text")

        self.extr_text_set = True
        self.extr_lic(doc).text = str_from_text(text)
        return True

    def set_lic_name(self, doc, name):
        """
        Set license name.
        Raise SPDXValueError if name is not str or utils.NoAssert
        Raise OrderError if no license id defined.
        """
        if not self.has_extr_lic(doc):
            raise OrderError("ExtractedLicense::Name")

        if self.extr_lic_name_set:
            raise CardinalityError("ExtractedLicense::Name")

        if not validations.validate_extr_lic_name(name):
            raise SPDXValueError("ExtractedLicense::Name")

        self.extr_lic_name_set = True
        self.extr_lic(doc).full_name = name
        return True

    def set_lic_comment(self, doc, comment):
        """
        Set license comment.
        Raise SPDXValueError if comment is not free form text or single line of text.
        Raise OrderError if no license ID defined.
        """
        if not self.has_extr_lic(doc):
            raise OrderError("ExtractedLicense::comment")

        if self.extr_lic_comment_set:
            raise CardinalityError("ExtractedLicense::comment")

        if not validations.validate_is_free_form_text_or_str(comment):
            raise SPDXValueError("ExtractedLicense::comment")

        self.extr_lic_comment_set = True
        self.extr_lic(doc).comment = str_from_text(comment)
        return True

    def add_lic_xref(self, doc, ref):
        """
        Add a license cross reference.
        Raise OrderError if no License ID defined.
        """
        if not self.has_extr_lic(doc):
            raise OrderError("ExtractedLicense::CrossRef")

        self.extr_lic(doc).add_xref(ref)
        return True

    def reset_extr_lics(self):
        # FIXME: this state does not make sense
        self.extr_text_set = False
        self.extr_lic_name_set = False
        self.extr_lic_comment_set = False


class SnippetBuilder(object):
    def __init__(self):
        # FIXME: this state does not make sense
        self.reset_snippet()

    def create_snippet(self, doc, spdx_id):
        """
        Create a snippet for the SPDX Document.
        spdx_id - To uniquely identify any element in an SPDX document which
        may be referenced by other elements.
        Raise SPDXValueError if the data is a malformed value.
        """
        self.reset_snippet()
        spdx_id = spdx_id.split("#")[-1]
        if not validations.validate_snippet_spdx_id(spdx_id):
            raise SPDXValueError("Snippet::SnippetSPDXID")

        self.snippet_spdx_id_set = True
        doc.add_snippet(snippet.Snippet(spdx_id=spdx_id))
        return True

    def set_snippet_name(self, doc, name):
        """
        Set name of the snippet.
        Raise OrderError if no snippet previously defined.
        Raise CardinalityError if the name is already set.
        """
        self.assert_snippet_exists()
        if self.snippet_name_set:
            raise CardinalityError("SnippetName")

        self.snippet_name_set = True
        doc.snippet[-1].name = name
        return True

    def set_snippet_comment(self, doc, comment):
        """
        Set general comments about the snippet.
        Raise OrderError if no snippet previously defined.
        Raise SPDXValueError if the data is not free form text or single line of text.
        Raise CardinalityError if comment already set.
        """
        self.assert_snippet_exists()
        if self.snippet_comment_set:
            raise CardinalityError("Snippet::SnippetComment")

        if not validations.validate_snip_comment(comment):
            raise SPDXValueError("Snippet::SnippetComment")

        self.snippet_comment_set = True
        doc.snippet[-1].comment = str_from_text(comment)
        return True

    def set_snippet_attribution_text(self, doc, text):
        """
        Set the snippet's attribution text .
        Raise SPDXValueError if text is not free form text or single line of text.
        """
        self.assert_snippet_exists()
        if not validations.validate_snippet_attribution_text(text):
            raise SPDXValueError("Snippet::AttributionText")

        doc.snippet[-1].attribution_text = str_from_text(text)
        return True

    def set_snippet_copyright(self, doc, text):
        """Set the snippet's copyright text.
        Raise OrderError if no snippet previously defined.
        Raise CardinalityError if already set.
        Raise SPDXValueError if text is not one of [None, NOASSERT, TEXT] or single line of text.
        """
        self.assert_snippet_exists()
        if self.snippet_copyright_set:
            raise CardinalityError("Snippet::SnippetCopyrightText")

        if not validations.validate_snippet_copyright(text, optional=True):
            raise SPDXValueError("Snippet::SnippetCopyrightText")

        self.snippet_copyright_set = True
        if isinstance(text, str):
            doc.snippet[-1].copyright = str_from_text(text)
        else:
            doc.snippet[-1].copyright = text  # None or NoAssert
        return True

    def set_snippet_lic_comment(self, doc, text):
        """
        Set the snippet's license comment.
        Raise OrderError if no snippet previously defined.
        Raise CardinalityError if already set.
        Raise SPDXValueError if the data is not free form text or single line of text.
        """
        self.assert_snippet_exists()
        if self.snippet_lic_comment_set:
            raise CardinalityError("Snippet::SnippetLicenseComments")

        if not validations.validate_snip_lic_comment(text):
            raise SPDXValueError("Snippet::SnippetLicenseComments")

        self.snippet_lic_comment_set = True
        doc.snippet[-1].license_comment = str_from_text(text)
        return True

    def set_snip_from_file_spdxid(self, doc, snip_from_file_spdxid):
        """
        Set the snippet's 'Snippet from File SPDX Identifier'.
        Raise OrderError if no snippet previously defined.
        Raise CardinalityError if already set.
        Raise SPDXValueError if the data is a malformed value.
        """
        self.assert_snippet_exists()
        snip_from_file_spdxid = snip_from_file_spdxid.split("#")[-1]
        if self.snip_file_spdxid_set:
            raise CardinalityError("Snippet::SnippetFromFileSPDXID")

        if not validations.validate_snip_file_spdxid(snip_from_file_spdxid):
            raise SPDXValueError("Snippet::SnippetFromFileSPDXID")

        self.snip_file_spdxid_set = True
        doc.snippet[-1].snip_from_file_spdxid = snip_from_file_spdxid
        return True

    def set_snip_concluded_license(self, doc, conc_lics):
        """
        Raise OrderError if no snippet previously defined.
        Raise CardinalityError if already set.
        Raise SPDXValueError if the data is a malformed value.
        """
        self.assert_snippet_exists()
        if self.snippet_conc_lics_set:
            raise CardinalityError("Snippet::SnippetLicenseConcluded")

        if not validations.validate_lics_conc(conc_lics, optional=True):
            raise SPDXValueError("Snippet::SnippetLicenseConcluded")

        self.snippet_conc_lics_set = True
        doc.snippet[-1].conc_lics = conc_lics
        return True

    def set_snippet_lics_info(self, doc, lics_info):
        """
        Raise OrderError if no snippet previously defined.
        Raise SPDXValueError if the data is a malformed value.
        """
        self.assert_snippet_exists()
        if not validations.validate_snip_lics_info(lics_info, optional=True):
            raise SPDXValueError("Snippet::LicenseInfoInSnippet")

        doc.snippet[-1].add_lics(lics_info)
        return True

    def set_snippet_byte_range(self, doc, parsed):
        """
        Raise OrderError if no snippet previously defined.
        Raise SPDXValueError if the data is malformed.
        """
        self.assert_snippet_exists()
        startpoint = int(parsed.split(":")[0])
        endpoint = int(parsed.split(":")[-1])
        if startpoint <= endpoint:
            doc.snippet[-1].byte_range = (startpoint, endpoint)
        else:
            raise SPDXValueError("Snippet::ByteRange")

    def set_snippet_line_range(self, doc, parsed):
        """
        Raise OrderError if no snippet previously defined.
        Raise SPDXValueError if the data is malformed.
        """
        self.assert_snippet_exists()
        startpoint = int(parsed.split(":")[0])
        endpoint = int(parsed.split(":")[-1])
        if startpoint <= endpoint:
            doc.snippet[-1].line_range = (startpoint, endpoint)
        else:
            raise SPDXValueError("Snippet::LineRange")

    def reset_snippet(self):
        # FIXME: this state does not make sense
        self.snippet_spdx_id_set = False
        self.snippet_name_set = False
        self.snippet_comment_set = False
        self.snippet_copyright_set = False
        self.snippet_lic_comment_set = False
        self.snip_file_spdxid_set = False
        self.snippet_conc_lics_set = False

    def assert_snippet_exists(self):
        if not self.snippet_spdx_id_set:
            raise OrderError("Snippet")


class Builder(
    DocBuilder,
    CreationInfoBuilder,
    EntityBuilder,
    ReviewBuilder,
    PackageBuilder,
    FileBuilder,
    LicenseBuilder,
    SnippetBuilder,
    ExternalDocumentRefBuilder,
    AnnotationBuilder,
    RelationshipBuilder,
):
    """
    SPDX document builder.
    """

    def __init__(self):
        super(Builder, self).__init__()
        # FIXME: this state does not make sense
        self.reset()
        self.current_package: Dict = dict()
        self.current_file: Dict = dict()

    def set_current_package_name(self, name: str) -> None:
        self.current_package["name"] = name

    def set_current_file_name(self, name: str) -> None:
        self.current_file["name"] = name

    def set_current_file_id(self, spdx_id: str) -> None:
        self.current_file["spdx_id"] = spdx_id

    def set_current_package_id(self, spdx_id: str) -> None:
        self.current_package["spdx_id"] = spdx_id

    def current_package_has_name(self) -> bool:
        return bool(("name" in self.current_package) and (self.current_package["name"]))

    def current_file_has_name(self) -> bool:
        return bool(("name" in self.current_file) and (self.current_file["name"]))

    def current_package_has_id(self) -> bool:
        return bool("spdx_id" in self.current_package) and (self.current_package["spdx_id"])

    def current_file_has_id(self) -> bool:
        return bool("spdx_id" in self.current_file) and (self.current_file["spdx_id"])

    def has_current_package(self) -> bool:
        return bool(self.current_package)

    def reset(self):
        """
        Reset builder's state for building new documents.
        Must be called between usage with different documents.
        """
        # FIXME: this state does not make sense
        self.reset_creation_info()
        self.reset_document()
        self.reset_package()
        self.reset_file_stat()
        self.reset_reviews()
        self.reset_annotations()
        self.reset_extr_lics()
        self.reset_snippet()
        self.reset_relationship()
