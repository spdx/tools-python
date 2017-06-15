
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

import re

from six import string_types

from spdx import checksum
from spdx import creationinfo
from spdx import document
from spdx import file
from spdx import package
from spdx import review
from spdx import utils
from spdx import version

from spdx.parsers.builderexceptions import CardinalityError
from spdx.parsers.builderexceptions import OrderError
from spdx.parsers.builderexceptions import SPDXValueError
from spdx.parsers.builderexceptions import IncompatibleVersionError
from spdx.parsers import validations


def checksum_from_sha1(value):
    """
    Return an spdx.checksum.Algorithm instance representing the SHA1
    checksum or None if does not match CHECKSUM_RE.
    """
    # More constrained regex at lexer level
    CHECKSUM_RE = re.compile('SHA1:\s*([\S]+)', re.UNICODE)
    match = CHECKSUM_RE.match(value)
    if match:
        return checksum.Algorithm(identifier='SHA1', value=match.group(1))
    else:
        return None


def str_from_text(text):
    """
    Return content of a free form text block as a string.
    """
    REGEX = re.compile('<text>((.|\n)+)</text>', re.UNICODE)
    match = REGEX.match(text)
    if match:
        return match.group(1)
    else:
        return None


class DocBuilder(object):
    """
    Responsible for setting the fields of the top level document model.
    """
    VERS_STR_REGEX = re.compile(r'SPDX-(\d+)\.(\d+)', re.UNICODE)

    def __init__(self):
        # FIXME: this state does not make sense
        self.reset_document()

    def set_doc_version(self, doc, value):
        """
        Set the document version.
        Raise SPDXValueError if malformed value, CardinalityError
        if already defined, IncompatibleVersionError v
        """
        # FIXME: we support other versions!!!
        if not self.doc_version_set:
            self.doc_version_set = True
            m = self.VERS_STR_REGEX.match(value)
            if m is None:
                raise SPDXValueError('Document::Version')
            else:
                vers = version.Version(major=int(m.group(1)),
                                       minor=int(m.group(2)))
                if vers == version.Version(major=1, minor=2):
                    doc.version = vers
                    return True
                else:
                    raise IncompatibleVersionError(value)
        else:
            raise CardinalityError('Document::Version')

    def set_doc_data_lics(self, doc, lics):
        """Sets the document data license.
        Raises value error if malformed value, CardinalityError
        if already defined.
        """
        if not self.doc_data_lics_set:
            self.doc_data_lics_set = True
            if validations.validate_data_lics(lics):
                doc.data_license = document.License.from_identifier(lics)
                return True
            else:
                raise SPDXValueError('Document::DataLicense')
        else:
            raise CardinalityError('Document::DataLicense')

    def set_doc_comment(self, doc, comment):
        """Sets document comment, Raises CardinalityError if
        comment already set.
        Raises SPDXValueError if comment is not free form text.
        """
        if not self.doc_comment_set:
            self.doc_comment_set = True
            if validations.validate_doc_comment(comment):
                doc.comment = str_from_text(comment)
                return True
            else:
                raise SPDXValueError('Document::Comment')
        else:
            raise CardinalityError('Document::Comment')

    def reset_document(self):
        """Resets the state to allow building new documents"""
        # FIXME: this state does not make sense
        self.doc_version_set = False
        self.doc_comment_set = False
        self.doc_data_lics_set = False


class EntityBuilder(object):

    tool_re = re.compile(r'Tool:\s*(.+)', re.UNICODE)
    person_re = re.compile(r'Person:\s*(([^(])+)(\((.*)\))?', re.UNICODE)
    org_re = re.compile(r'Organization:\s*(([^(])+)(\((.*)\))?', re.UNICODE)
    PERSON_NAME_GROUP = 1
    PERSON_EMAIL_GROUP = 4
    ORG_NAME_GROUP = 1
    ORG_EMAIL_GROUP = 4
    TOOL_NAME_GROUP = 1

    def build_tool(self, doc, entity):
        """Builds a tool object out of a string representation.
        Returns built tool. Raises SPDXValueError if failed to extract
        tool name or name is malformed
        """
        match = self.tool_re.match(entity)
        if match and validations.validate_tool_name(match.group(self.TOOL_NAME_GROUP)):
            name = match.group(self.TOOL_NAME_GROUP)
            return creationinfo.Tool(name)
        else:
            raise SPDXValueError('Failed to extract tool name')

    def build_org(self, doc, entity):
        """Builds an organization object of of a string representation.
        Returns built organization. Raises SPDXValueError if failed to extract
        name.
        """
        match = self.org_re.match(entity)
        if match and validations.validate_org_name(match.group(self.ORG_NAME_GROUP)):
            name = match.group(self.ORG_NAME_GROUP).strip()
            email = match.group(self.ORG_EMAIL_GROUP)
            if (email is not None) and (len(email) != 0):
                return creationinfo.Organization(name=name, email=email.strip())
            else:
                return creationinfo.Organization(name=name, email=None)
        else:
            raise SPDXValueError('Failed to extract Organization name')

    def build_person(self, doc, entity):
        """Builds an organization object of of a string representation.
        Returns built organization. Raises SPDXValueError if failed to extract
        name.
        """
        match = self.person_re.match(entity)
        if match and validations.validate_person_name(match.group(self.PERSON_NAME_GROUP)):
            name = match.group(self.PERSON_NAME_GROUP).strip()
            email = match.group(self.PERSON_EMAIL_GROUP)
            if (email is not None) and (len(email) != 0):
                return creationinfo.Person(name=name, email=email.strip())
            else:
                return creationinfo.Person(name=name, email=None)
        else:
            raise SPDXValueError('Failed to extract person name')


class CreationInfoBuilder(object):

    def __init__(self):
        # FIXME: this state does not make sense
        self.reset_creation_info()

    def add_creator(self, doc, creator):
        """Adds a creator to the document's creation info.
        Returns true if creator is valid.
        Creator must be built by an EntityBuilder.
        Raises SPDXValueError if not a creator type.
        """
        if validations.validate_creator(creator):
            doc.creation_info.add_creator(creator)
            return True
        else:
            raise SPDXValueError('CreationInfo::Creator')

    def set_created_date(self, doc, created):
        """Sets created date, Raises CardinalityError if
        created date already set.
        Raises SPDXValueError if created is not a date.
        """
        if not self.created_date_set:
            self.created_date_set = True
            date = utils.datetime_from_iso_format(created)
            if date is not None:
                doc.creation_info.created = date
                return True
            else:
                raise SPDXValueError('CreationInfo::Date')
        else:
            raise CardinalityError('CreationInfo::Created')

    def set_creation_comment(self, doc, comment):
        """Sets creation comment, Raises CardinalityError if
        comment already set.
        Raises SPDXValueError if not free form text.
        """
        if not self.creation_comment_set:
            self.creation_comment_set = True
            if validations.validate_creation_comment(comment):
                doc.creation_info.comment = str_from_text(comment)
                return True
            else:
                raise SPDXValueError('CreationInfo::Comment')
        else:
            raise CardinalityError('CreationInfo::Comment')

    def set_lics_list_ver(self, doc, value):
        """Sets the license list version, Raises CardinalityError if
        already set, SPDXValueError if incorrect value.
        """
        if not self.lics_list_ver_set:
            self.lics_list_ver_set = True
            vers = version.Version.from_str(value)
            if vers is not None:
                doc.creation_info.license_list_version = vers
                return True
            else:
                raise SPDXValueError('CreationInfo::LicenseListVersion')
        else:
            raise CardinalityError('CreationInfo::LicenseListVersion')

    def reset_creation_info(self):
        """
        Resets builder state to allow building new creation info."""
        # FIXME: this state does not make sense
        self.created_date_set = False
        self.creation_comment_set = False
        self.lics_list_ver_set = False


class ReviewBuilder(object):

    def __init__(self):
        # FIXME: this state does not make sense
        self.reset_reviews()

    def reset_reviews(self):
        """Resets the builder's state to allow building new reviews."""
        # FIXME: this state does not make sense
        self.review_date_set = False
        self.review_comment_set = False

    def add_reviewer(self, doc, reviewer):
        """Adds a reviewer to the SPDX Document.
        Reviwer is an entity created by an EntityBuilder.
        Raises SPDXValueError if not a valid reviewer type.
        """
        # Each reviewer marks the start of a new review object.
        # FIXME: this state does not make sense
        self.reset_reviews()
        if validations.validate_reviewer(reviewer):
            doc.add_review(review.Review(reviewer=reviewer))
            return True
        else:
            raise SPDXValueError('Review::Reviewer')

    def add_review_date(self, doc, reviewed):
        """Sets the review date. Raises CardinalityError if
        already set. OrderError if no reviewer defined before.
        Raises SPDXValueError if invalid reviewed value.
        """
        if len(doc.reviews) != 0:
            if not self.review_date_set:
                self.review_date_set = True
                date = utils.datetime_from_iso_format(reviewed)
                if date is not None:
                    doc.reviews[-1].review_date = date
                    return True
                else:
                    raise SPDXValueError('Review::ReviewDate')
            else:
                raise CardinalityError('Review::ReviewDate')
        else:
            raise OrderError('Review::ReviewDate')

    def add_review_comment(self, doc, comment):
        """Sets the review comment. Raises CardinalityError if
        already set. OrderError if no reviewer defined before.
        Raises SPDXValueError if comment is not free form text.
        """
        if len(doc.reviews) != 0:
            if not self.review_comment_set:
                self.review_comment_set = True
                if validations.validate_review_comment(comment):
                    doc.reviews[-1].comment = str_from_text(comment)
                    return True
                else:
                    raise SPDXValueError('ReviewComment::Comment')
            else:
                raise CardinalityError('ReviewComment')
        else:
            raise OrderError('ReviewComment')


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
        self.package_vers_set = False
        self.package_file_name_set = False
        self.package_supplier_set = False
        self.package_originator_set = False
        self.package_down_location_set = False
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

    def create_package(self, doc, name):
        """Creates a package for the SPDX Document.
        name - any string.
        Raises CardinalityError if package already defined.
        """
        if not self.package_set:
            self.package_set = True
            doc.package = package.Package(name=name)
            return True
        else:
            raise CardinalityError('Package::Name')

    def set_pkg_vers(self, doc, version):
        """Sets package version, if not already set.
        version - Any string.
        Raises CardinalityError if already has a version.
        Raises OrderError if no package previously defined.
        """
        self.assert_package_exists()
        if not self.package_vers_set:
            self.package_vers_set = True
            doc.package.version = version
            return True
        else:
            raise CardinalityError('Package::Version')

    def set_pkg_file_name(self, doc, name):
        """Sets the package file name, if not already set.
        name - Any string.
        Raises CardinalityError if already has a file_name.
        Raises OrderError if no pacakge previously defined.
        """
        self.assert_package_exists()
        if not self.package_file_name_set:
            self.package_file_name_set = True
            doc.package.file_name = name
            return True
        else:
            raise CardinalityError('Package::FileName')

    def set_pkg_supplier(self, doc, entity):
        """Sets the package supplier, if not already set.
        entity - Organization, Person or NoAssert.
        Raises CardinalityError if already has a supplier.
        Raises OrderError if no package previously defined.
        """
        self.assert_package_exists()
        if not self.package_supplier_set:
            self.package_supplier_set = True
            if validations.validate_pkg_supplier(entity):
                doc.package.supplier = entity
                return True
            else:
                raise SPDXValueError('Package::Supplier')
        else:
            raise CardinalityError('Package::Supplier')

    def set_pkg_originator(self, doc, entity):
        """Sets the package originator, if not already set.
        entity - Organization, Person or NoAssert.
        Raises CardinalityError if already has an originator.
        Raises OrderError if no package previously defined.
        """
        self.assert_package_exists()
        if not self.package_originator_set:
            self.package_originator_set = True
            if validations.validate_pkg_originator(entity):
                doc.package.originator = entity
                return True
            else:
                raise SPDXValueError('Package::Originator')
        else:
            raise CardinalityError('Package::Originator')

    def set_pkg_down_location(self, doc, location):
        """Sets the package download location, if not already set.
        location - A string
        Raises CardinalityError if already defined.
        Raises OrderError if no package previously defined.
        """
        self.assert_package_exists()
        if not self.package_down_location_set:
            self.package_down_location_set = True
            doc.package.download_location = location
            return True
        else:
            raise CardinalityError('Package::DownloadLocation')

    def set_pkg_home(self, doc, location):
        """Sets the package homepage location if not already set.
        location - A string or None or NoAssert.
        Raises CardinalityError if already defined.
        Raises OrderError if no package previously defined.
        Raises SPDXValueError if location has incorrect value.
        """
        self.assert_package_exists()
        if not self.package_home_set:
            self.package_home_set = True
            if validations.validate_pkg_homepage(location):
                doc.package.homepage = location
                return True
            else:
                raise SPDXValueError('Package::HomePage')
        else:
            raise CardinalityError('Package::HomePage')

    def set_pkg_verif_code(self, doc, code):
        """Sets the package verification code, if not already set.
        code - A string.
        Raises CardinalityError if already defined.
        Raises OrderError if no package previously defined.
        Raises Value error if doesn't match verifcode form
        """
        self.assert_package_exists()
        if not self.package_verif_set:
            self.package_verif_set = True
            match = self.VERIF_CODE_REGEX.match(code)
            if match:
                doc.package.verif_code = match.group(self.VERIF_CODE_CODE_GRP)
                if match.group(self.VERIF_CODE_EXC_FILES_GRP) is not None:
                    doc.package.verif_exc_files = match.group(self.VERIF_CODE_EXC_FILES_GRP).split(',')
                return True
            else:
                raise SPDXValueError('Package::VerificationCode')
        else:
            raise CardinalityError('Package::VerificationCode')

    def set_pkg_chk_sum(self, doc, chk_sum):
        """Sets the package check sum, if not already set.
        chk_sum - A string
        Raises CardinalityError if already defined.
        Raises OrderError if no package previously defined.
        """
        self.assert_package_exists()
        if not self.package_chk_sum_set:
            self.package_chk_sum_set = True
            doc.package.check_sum = checksum_from_sha1(chk_sum)
            return True
        else:
            raise CardinalityError('Package::CheckSum')

    def set_pkg_source_info(self, doc, text):
        """Sets the package's source information, if not already set.
        text - Free form text.
        Raises CardinalityError if already defined.
        Raises OrderError if no package previously defined.
        SPDXValueError if text is not free form text.
        """
        self.assert_package_exists()
        if not self.package_source_info_set:
            self.package_source_info_set = True
            if validations.validate_pkg_src_info(text):
                doc.package.source_info = str_from_text(text)
                return True
            else:
                raise SPDXValueError('Pacckage::SourceInfo')
        else:
            raise CardinalityError('Package::SourceInfo')

    def set_pkg_licenses_concluded(self, doc, licenses):
        """Sets the package's concluded licenses.
        licenses - License info.
        Raises CardinalityError if already defined.
        Raises OrderError if no package previously defined.
        Raises SPDXValueError if data malformed.
        """
        self.assert_package_exists()
        if not self.package_conc_lics_set:
            self.package_conc_lics_set = True
            if validations.validate_lics_conc(licenses):
                doc.package.conc_lics = licenses
                return True
            else:
                raise SPDXValueError('Package::ConcludedLicenses')
        else:
            raise CardinalityError('Package::ConcludedLicenses')

    def set_pkg_license_from_file(self, doc, lic):
        """Adds a license from a file to the package.
        Raises SPDXValueError if data malformed.
        Raises OrderError if no package previously defined.
        """
        self.assert_package_exists()
        if validations.validate_lics_from_file(lic):
            doc.package.licenses_from_files.append(lic)
            return True
        else:
            raise SPDXValueError('Package::LicensesFromFile')

    def set_pkg_license_declared(self, doc, lic):
        """Sets the package's declared license.
        Raises SPDXValueError if data malformed.
        Raises OrderError if no package previously defined.
        Raises CardinalityError if already set.
        """
        self.assert_package_exists()
        if not self.package_license_declared_set:
            self.package_license_declared_set = True
            if validations.validate_lics_conc(lic):
                doc.package.license_declared = lic
                return True
            else:
                raise SPDXValueError('Package::LicenseDeclared')
        else:
            raise CardinalityError('Package::LicenseDeclared')

    def set_pkg_license_comment(self, doc, text):
        """Sets the package's license comment.
        Raises OrderError if no package previously defined.
        Raises CardinalityError if already set.
        Raises SPDXValueError if text is not free form text.
        """
        self.assert_package_exists()
        if not self.package_license_comment_set:
            self.package_license_comment_set = True
            if validations.validate_pkg_lics_comment(text):
                doc.package.license_comment = str_from_text(text)
                return True
            else:
                raise SPDXValueError('Package::LicenseComment')
        else:
            raise CardinalityError('Package::LicenseComment')

    def set_pkg_cr_text(self, doc, text):
        """Sets the package's license comment.
        Raises OrderError if no package previously defined.
        Raises CardinalityError if already set.
        Raises value error if text is not one of [None, NOASSERT, TEXT].
        """
        self.assert_package_exists()
        if not self.package_cr_text_set:
            self.package_cr_text_set = True
            if validations.validate_pkg_cr_text(text):
                if isinstance(text, string_types):
                    doc.package.cr_text = str_from_text(text)
                else:
                    doc.package.cr_text = text  # None or NoAssert
            else:
                raise SPDXValueError('Package::CopyrightText')
        else:
            raise CardinalityError('Package::CopyrightText')

    def set_pkg_summary(self, doc, text):
        """Set's the package summary.
        Raises SPDXValueError if text is not free form text.
        Raises CardinalityError if summary already set.
        Raises OrderError if no package previously defined.
        """
        self.assert_package_exists()
        if not self.package_summary_set:
            self.package_summary_set = True
            if validations.validate_pkg_summary(text):
                doc.package.summary = str_from_text(text)
            else:
                raise SPDXValueError('Package::Summary')
        else:
            raise CardinalityError('Package::Summary')

    def set_pkg_desc(self, doc, text):
        """Set's the package's description.
        Raises SPDXValueError if text is not free form text.
        Raises CardinalityError if description already set.
        Raises OrderError if no package previously defined.
        """
        self.assert_package_exists()
        if not self.package_desc_set:
            self.package_desc_set = True
            if validations.validate_pkg_desc(text):
                doc.package.description = str_from_text(text)
            else:
                raise SPDXValueError('Package::Description')
        else:
            raise CardinalityError('Package::Description')

    def assert_package_exists(self):
        if not self.package_set:
            raise OrderError('Package')


class FileBuilder(object):

    def __init__(self):
        # FIXME: this state does not make sense
        self.reset_file_stat()

    def set_file_name(self, doc, name):
        """Raises OrderError if no package defined.
        """
        if self.has_package(doc):
            doc.package.files.append(file.File(name))
            # A file name marks the start of a new file instance.
            # The builder must be reset
            # FIXME: this state does not make sense
            self.reset_file_stat()
            return True
        else:
            raise OrderError('File::Name')

    def set_file_comment(self, doc, text):
        """
        Raises OrderError if no package or no file defined.
        Raises CardinalityError if more than one comment set.
        Raises SPDXValueError if text is not free form text.
        """
        if self.has_package(doc) and self.has_file(doc):
            if not self.file_comment_set:
                self.file_comment_set = True
                if validations.validate_file_comment(text):
                    self.file(doc).comment = str_from_text(text)
                    return True
                else:
                    raise SPDXValueError('File::Comment')
            else:
                raise CardinalityError('File::Comment')
        else:
            raise OrderError('File::Comment')

    def set_file_type(self, doc, type_value):
        """
        Raises OrderError if no package or file defined.
        Raises CardinalityError if more than one type set.
        Raises SPDXValueError if type is unknown.
        """
        type_dict = {
            'SOURCE': file.FileType.SOURCE,
            'BINARY': file.FileType.BINARY,
            'ARCHIVE': file.FileType.ARCHIVE,
            'OTHER': file.FileType.OTHER
        }
        if self.has_package(doc) and self.has_file(doc):
            if not self.file_type_set:
                self.file_type_set = True
                if type_value in type_dict.keys():
                    self.file(doc).type = type_dict[type_value]
                    return True
                else:
                    raise SPDXValueError('File::Type')
            else:
                raise CardinalityError('File::Type')
        else:
            raise OrderError('File::Type')

    def set_file_chksum(self, doc, chksum):
        """
        Raises OrderError if no package or file defined.
        Raises CardinalityError if more than one chksum set.
        """
        if self.has_package(doc) and self.has_file(doc):
            if not self.file_chksum_set:
                self.file_chksum_set = True
                self.file(doc).chk_sum = checksum_from_sha1(chksum)
                return True
            else:
                raise CardinalityError('File::CheckSum')
        else:
            raise OrderError('File::CheckSum')

    def set_concluded_license(self, doc, lic):
        """
        Raises OrderError if no package or file defined.
        Raises CardinalityError if already set.
        Raises SPDXValueError if malformed.
        """
        if self.has_package(doc) and self.has_file(doc):
            if not self.file_conc_lics_set:
                self.file_conc_lics_set = True
                if validations.validate_lics_conc(lic):
                    self.file(doc).conc_lics = lic
                    return True
                else:
                    raise SPDXValueError('File::ConcludedLicense')
            else:
                raise CardinalityError('File::ConcludedLicense')
        else:
            raise OrderError('File::ConcludedLicense')

    def set_file_license_in_file(self, doc, lic):
        """
        Raises OrderError if no package or file defined.
        Raises SPDXValueError if malformed value.
        """
        if self.has_package(doc) and self.has_file(doc):
            if validations.validate_file_lics_in_file(lic):
                self.file(doc).add_lics(lic)
                return True
            else:
                raise SPDXValueError('File::LicenseInFile')
        else:
            raise OrderError('File::LicenseInFile')

    def set_file_license_comment(self, doc, text):
        """
        Raises OrderError if no package or file defined.
        Raises SPDXValueError if text is not free form text.
        Raises CardinalityError if more than one per file.
        """
        if self.has_package(doc) and self.has_file(doc):
            if not self.file_license_comment_set:
                self.file_license_comment_set = True
                if validations.validate_file_lics_comment(text):
                    self.file(doc).license_comment = str_from_text(text)
                else:
                    raise SPDXValueError('File::LicenseComment')
            else:
                raise CardinalityError('File::LicenseComment')
        else:
            raise OrderError('File::LicenseComment')

    def set_file_copyright(self, doc, text):
        """Raises OrderError if no package or file defined.
        Raises SPDXValueError if not free form text or NONE or NO_ASSERT.
        Raises CardinalityError if more than one.
        """
        if self.has_package(doc) and self.has_file(doc):
            if not self.file_copytext_set:
                self.file_copytext_set = True
                if validations.validate_file_cpyright(text):
                    if isinstance(text, string_types):
                        self.file(doc).copyright = str_from_text(text)
                    else:
                        self.file(doc).copyright = text  # None or NoAssert
                    return True
                else:
                    raise SPDXValueError('File::CopyRight')
            else:
                raise CardinalityError('File::CopyRight')
        else:
            raise OrderError('File::CopyRight')

    def set_file_notice(self, doc, text):
        """Raises OrderError if no package or file defined.
        Raises SPDXValueError if not free form text.
        Raises CardinalityError if more than one.
        """
        if self.has_package(doc) and self.has_file(doc):
            if not self.file_notice_set:
                self.file_notice_set = True
                if validations.validate_file_notice(text):
                    self.file(doc).notice = str_from_text(text)
                else:
                    raise SPDXValueError('File::Notice')
            else:
                raise CardinalityError('File::Notice')
        else:
            raise OrderError('File::Notice')

    def add_file_contribution(self, doc, value):
        """Raises OrderError if no package or file defined.
        """
        if self.has_package(doc) and self.has_file(doc):
            self.file(doc).add_contrib(value)
        else:
            raise OrderError('File::Contributor')

    def add_file_dep(self, doc, value):
        """Raises OrderError if no package or file defined.
        """
        if self.has_package(doc) and self.has_file(doc):
            self.file(doc).add_depend(value)
        else:
            raise OrderError('File::Dependency')

    def set_file_atrificat_of_project(self, doc, symbol, value):
        """Sets a file name, uri or home artificat.
        Raises OrderError if no package or file defined.
        """
        if self.has_package(doc) and self.has_file(doc):
            self.file(doc).add_artifact(symbol, value)
        else:
            raise OrderError('File::Artificat')


    def file(self, doc):
        """Returns the last file in the document's package's file list."""
        return doc.package.files[-1]

    def has_file(self, doc):
        """Returns true if the document's package has at least one file.
        Does not test if the document has a package.
        """
        return len(doc.package.files) != 0

    def has_package(self, doc):
        """Returns true if the document has a package."""
        return doc.package is not None

    def reset_file_stat(self):
        """Resets the builder's state to enable building new files."""
        # FIXME: this state does not make sense
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
        """Retrieves last license in extracted license list"""
        return doc.extracted_licenses[-1]

    def has_extr_lic(self, doc):
        return len(doc.extracted_licenses) != 0

    def set_lic_id(self, doc, lic_id):
        """Adds a new extracted license to the document.
        Raises SPDXValueError if data format is incorrect.
        """
        # FIXME: this state does not make sense
        self.reset_extr_lics()
        if validations.validate_extracted_lic_id(lic_id):
            doc.add_extr_lic(document.ExtractedLicense(lic_id))
            return True
        else:
            raise SPDXValueError('ExtractedLicense::id')

    def set_lic_text(self, doc, text):
        """Sets license extracted text.
        Raises SPDXValueError if text is not free form text.
        Raises OrderError if no license ID defined.
        """
        if self.has_extr_lic(doc):
            if not self.extr_text_set:
                self.extr_text_set = True
                if validations.validate_is_free_form_text(text):
                    self.extr_lic(doc).text = str_from_text(text)
                    return True
                else:
                    raise SPDXValueError('ExtractedLicense::text')
            else:
                raise CardinalityError('ExtractedLicense::text')
        else:
            raise OrderError('ExtractedLicense::text')

    def set_lic_name(self, doc, name):
        """Sets license name.
        Raises SPDXValueError if name is not str or utils.NoAssert
        Raises OrderError if no license id defined.
        """
        if self.has_extr_lic(doc):
            if not self.extr_lic_name_set:
                self.extr_lic_name_set = True
                if validations.validate_extr_lic_name(name):
                    self.extr_lic(doc).full_name = name
                    return True
                else:
                    raise SPDXValueError('ExtractedLicense::Name')
            else:
                raise CardinalityError('ExtractedLicense::Name')
        else:
            raise OrderError('ExtractedLicense::Name')

    def set_lic_comment(self, doc, comment):
        """Sets license comment.
        Raises SPDXValueError if comment is not free form text.
        Raises OrderError if no license ID defined.
        """
        if self.has_extr_lic(doc):
            if not self.extr_lic_comment_set:
                self.extr_lic_comment_set = True
                if validations.validate_is_free_form_text(comment):
                    self.extr_lic(doc).comment = str_from_text(comment)
                    return True
                else:
                    raise SPDXValueError('ExtractedLicense::comment')
            else:
                raise CardinalityError('ExtractedLicense::comment')
        else:
            raise OrderError('ExtractedLicense::comment')

    def add_lic_xref(self, doc, ref):
        """Adds a license cross reference.
        Raises OrderError if no License ID defined.
        """
        if self.has_extr_lic(doc):
            self.extr_lic(doc).add_xref(ref)
            return True
        else:
            raise OrderError('ExtractedLicense::CrossRef')

    def reset_extr_lics(self):
        # FIXME: this state does not make sense
        self.extr_text_set = False
        self.extr_lic_name_set = False
        self.extr_lic_comment_set = False


class Builder(DocBuilder, CreationInfoBuilder, EntityBuilder, ReviewBuilder,
              PackageBuilder, FileBuilder, LicenseBuilder):

    """SPDX document builder."""

    def __init__(self):
        super(Builder, self).__init__()
        # FIXME: this state does not make sense
        self.reset()

    def reset(self):
        """Resets builder's state for building new documents.
        Must be called between usage with different documents.
        """
        # FIXME: this state does not make sense
        self.reset_creation_info()
        self.reset_document()
        self.reset_package()
        self.reset_file_stat()
        self.reset_reviews()
        self.reset_extr_lics()
