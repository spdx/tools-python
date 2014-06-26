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
import re
from .. import version
from .. import document
from .. import creationinfo
from .. import utils
from .. import review
from .. import package
from .. import file
from validations import *


class BuilderException(Exception):

    """Builder exception base class."""
    pass


class IncompatibleVersionError(BuilderException):

    def __init__(self, msg):
        self.msg = msg


class CardinalityError(BuilderException):

    def __init__(self, msg):
        self.msg = msg


class ValueError(BuilderException):

    def __init__(self, msg):
        self.msg = msg


class OrderError(BuilderException):

    def __init__(self, msg):
        self.msg = msg


def str_from_text(text):
    """Returns content of a free form text block as a python string."""
    REGEX = re.compile('<text>((.|\n)+)</text>')
    match = REGEX.match(text)
    if match:
        return match.group(1)
    else:
        return None


class DocBuilder(object):
    VERS_STR_REGEX = re.compile(r'SPDX-(\d+)\.(\d+)')

    def __init__(self):
        super(DocBuilder, self).__init__()
        self.doc_version_set = False
        self.doc_comment_set = False
        self.doc_data_lics_set = False

    def set_doc_version(self, doc, value):
        """Sets the document version. 
        Raises value error if malformed value, CardinalityError
        if already defined, IncompatibleVersionError if not 1.2.
        """
        if not self.doc_version_set:
            self.doc_version_set = True
            m = self.VERS_STR_REGEX.match(value)
            if m is None:
                raise ValueError('Document::Version')
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
            if validate_data_lics(lics):
                doc.data_license = document.License.from_identifier(lics)
                return True
            else:
                raise ValueError('Document::DataLicense')
        else:
            raise CardinalityError('Document::DataLicense')

    def set_doc_comment(self, doc, comment):
        """Sets document comment, Raises CardinalityError if
        comment already set.
        Raises ValueError if comment is not free form text.
        """
        if not self.doc_comment_set:
            self.doc_comment_set = True
            if validate_doc_comment(comment):
                doc.comment = str_from_text(comment)
                return True
            else:
                raise ValueError('Document::Comment')
        else:
            raise CardinalityError('Document::Comment')


class EntityBuilder(object):

    tool_re = re.compile(r'Tool:\s*(.+)', re.UNICODE)
    person_re = re.compile(r'Person:\s*((\w\s?)+)(\((.*)\))?', re.UNICODE)
    org_re = re.compile(r'Organization:\s*((\w\s?)+)(\((.*)\))?', re.UNICODE)
    PERSON_NAME_GROUP = 1
    PERSON_EMAIL_GROUP = 4
    ORG_NAME_GROUP = 1
    ORG_EMAIL_GROUP = 4
    TOOL_NAME_GROUP = 1

    def __init__(self):
        super(EntityBuilder, self).__init__()

    def build_tool(self, doc, entity):
        """Builds a tool object out of a string representation.
        Returns built tool. Raises ValueError if failed to extract
        tool name or name is malformed
        """
        match = self.tool_re.match(entity)
        if match and validate_tool_name(match.group(self.TOOL_NAME_GROUP)):
            name = match.group(self.TOOL_NAME_GROUP)
            return creationinfo.Tool(name)
        else:
            raise ValueError('Failed to extract tool name')

    def build_org(self, doc, entity):
        """Builds an organization object of of a string representation.
        Returns built organization. Raises ValueError if failed to extract
        name.
        """
        match = self.org_re.match(entity)
        if match and validate_org_name(match.group(self.ORG_NAME_GROUP)):
            name = match.group(self.ORG_NAME_GROUP).strip()
            email = match.group(self.ORG_EMAIL_GROUP)
            if (email is not None) and (len(email) != 0):
                return creationinfo.Organization(name=name, email=email.strip())
            else:
                return creationinfo.Organization(name=name, email=None)
        else:
            raise ValueError('Failed to extract Organization name')

    def build_person(self, doc, entity):
        """Builds an organization object of of a string representation.
        Returns built organization. Raises ValueError if failed to extract
        name.
        """
        match = self.person_re.match(entity)
        if match and validate_person_name(match.group(self.PERSON_NAME_GROUP)):
            name = match.group(self.PERSON_NAME_GROUP).strip()
            email = match.group(self.PERSON_EMAIL_GROUP)
            if (email is not None) and (len(email) != 0):
                return creationinfo.Person(name=name, email=email.strip())
            else:
                return creationinfo.Person(name=name, email=None)
        else:
            raise ValueError('Failed to extract person name')


class CreationInfoBuilder(object):

    def __init__(self):
        super(CreationInfoBuilder, self).__init__()
        self.created_date_set = False
        self.creation_comment_set = False
        self.lics_list_ver_set = False

    def add_creator(self, doc, creator):
        """Adds a creator to the document's creation info.
        Returns true if creator is valid.
        Creator must be built by an EntityBuilder.
        Raises ValueError if not a creator type.
        """
        if validate_creator(creator):
            doc.creation_info.add_creator(creator)
            return True
        else:
            raise ValueError('CreationInfo::Creator')

    def set_created_date(self, doc, created):
        """Sets created date, Raises CardinalityError if 
        created date already set.
        Raises ValueError if created is not a date.
        """
        if not self.created_date_set:
            self.created_date_set = True
            date = utils.datetime_from_iso_format(created)
            if date is not None:
                doc.creation_info.created = date
                return True
            else:
                raise ValueError('CreationInfo::Date')
        else:
            raise CardinalityError('CreationInfo::Created')

    def set_creation_comment(self, doc, comment):
        """Sets creation comment, Raises CardinalityError if
        comment already set.
        Raises ValueError if not free form text.
        """
        if not self.creation_comment_set:
            self.creation_comment_set = True
            if validate_creation_comment(comment):
                doc.creation_info.comment = str_from_text(comment)
                return True
            else:
                raise ValueError('CreationInfo::Comment')
        else:
            raise CardinalityError('CreationInfo::Comment')

    def set_lics_list_ver(self, doc, value):
        """Sets the license list version, Raises CardinalityError if
        already set, ValueError if incorrect value.
        """
        if not self.lics_list_ver_set:
            self.lics_list_ver_set = True
            vers = version.Version.from_str(value)
            if vers is not None:
                doc.creation_info.license_list_version = vers
                return True
            else:
                raise ValueError('CreationInfo::LicenseListVersion')
        else:
            raise CardinalityError('CreationInfo::LicenseListVersion')


class ReviewBuilder(object):

    def __init__(self):
        super(ReviewBuilder, self).__init__()
        self.review_date_set = False
        self.review_comment_set = False

    def add_reviewer(self, doc, reviewer):
        """Adds a reviewer to the SPDX Document.
        Reviwer is an entity created by an EntityBuilder.
        Raises ValueError if not a valid reviewer type.
        """
        self.review_date_set = False
        self.review_comment_set = False
        if validate_reviewer(reviewer):
            doc.add_review(review.Review(reviewer=reviewer))
            return True
        else:
            raise ValueError('Review::Reviewer')

    def add_review_date(self, doc, reviewed):
        """Sets the review date. Raises CardinalityError if 
        already set. OrderError if no reviewer defined before.
        Raises ValueError if invalid reviewed value.
        """
        if len(doc.reviews) != 0:
            if not self.review_date_set:
                self.review_date_set = True
                date = utils.datetime_from_iso_format(reviewed)
                if date is not None:
                    doc.reviews[-1].review_date = date
                    return True
                else:
                    raise ValueError('Review::ReviewDate')
            else:
                raise CardinalityError('Review::ReviewDate')
        else:
            raise OrderError('Review::ReviewDate')

    def add_review_comment(self, doc, comment):
        """Sets the review comment. Raises CardinalityError if 
        already set. OrderError if no reviewer defined before.
        Raises ValueError if comment is not free form text.
        """
        if len(doc.reviews) != 0:
            if not self.review_comment_set:
                self.review_comment_set = True
                if validate_review_comment(comment):
                    doc.reviews[-1].comment = str_from_text(comment)
                    return True
                else:
                    raise ValueError('ReviewComment::Comment')
            else:
                raise CardinalityError('ReviewComment')
        else:
            raise OrderError('ReviewComment')


class PackageBuilder(object):

    def __init__(self):
        super(PackageBuilder, self).__init__()
        self.reset_package()

    def reset_package(self):
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
            if validate_pkg_supplier(entity):
                doc.package.supplier = entity
                return True
            else:
                raise ValueError('Package::Supplier')
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
            if validate_pkg_originator(entity):
                doc.package.originator = entity
                return True
            else:
                raise ValueError('Package::Originator')
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
        Raises ValueError if location has incorrect value.
        """
        self.assert_package_exists()
        if not self.package_home_set:
            self.package_home_set = True
            if validate_pkg_homepage(location):
                doc.package.homepage = location
                return True
            else:
                raise ValueError('Package::HomePage')
        else:
            raise CardinalityError('Package::HomePage')

    def set_pkg_verif_code(self, doc, code):
        """Sets the package verification code, if not already set.
        code - A string.
        Raises CardinalityError if already defined.
        Raises OrderError if no package previously defined.
        """
        self.assert_package_exists()
        if not self.package_verif_set:
            self.package_verif_set = True
            doc.package.verif_code = code
            return True
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
            doc.package.check_sum = chk_sum
            return True
        else:
            raise CardinalityError('Package::CheckSum')

    def set_pkg_source_info(self, doc, text):
        """Sets the package's source information, if not already set.
        text - Free form text.
        Raises CardinalityError if already defined.
        Raises OrderError if no package previously defined.
        ValueError if text is not free form text.
        """
        self.assert_package_exists()
        if not self.package_source_info_set:
            self.package_source_info_set = True
            if validate_pkg_src_info(text):
                doc.package.source_info = str_from_text(text)
                return True
            else:
                raise ValueError('Pacckage::SourceInfo')
        else:
            raise CardinalityError('Package::SourceInfo')

    def set_pkg_licenses_concluded(self, doc, licenses):
        """Sets the package's concluded licenses.
        licenses - License info.
        Raises CardinalityError if already defined.
        Raises OrderError if no package previously defined.
        Raises ValueError if data malformed.
        """
        self.assert_package_exists()
        if not self.package_conc_lics_set:
            self.package_conc_lics_set = True
            if validate_lics_conc(licenses):
                doc.package.conc_lics = licenses
                return True
            else:
                raise ValueError('Package::ConcludedLicenses')
        else:
            raise CardinalityError('Package::ConcludedLicenses')

    def set_pkg_license_from_file(self, doc, license):
        """Adds a license from a file to the package.
        Raises ValueError if data malformed.
        Raises OrderError if no package previously defined.
        """
        self.assert_package_exists()
        if validate_lics_from_file(license):
            if license == 'NO_ASSERT':
                doc.package.licenses_from_files.append(utils.NoAssert())
            elif license == 'NONE':
                doc.package.licenses_from_files.append(utils.None())
            else:
                doc.package.licenses_from_files.append(
                    document.License.from_identifier(license))
            return True
        else:
            raise ValueError('Package::LicensesFromFile')

    def set_pkg_license_declared(self, doc, license):
        """Sets the package's declared license.
        Raises ValueError if data malformed.
        Raises OrderError if no package previously defined.
        Raises CardinalityError if already set.
        """
        self.assert_package_exists()
        if not self.package_license_declared_set:
            self.package_license_declared_set = True
            if validate_lics_conc(license):
                doc.package.license_declared = license
                return True
            else:
                raise ValueError('Package::LicenseDeclared')
        else:
            raise CardinalityError('Package::LicenseDeclared')

    def set_pkg_license_comment(self, doc, text):
        """Sets the package's license comment.
        Raises OrderError if no package previously defined.
        Raises CardinalityError if already set.
        Raises ValueError if text is not free form text.
        """
        self.assert_package_exists()
        if not self.package_license_comment_set:
            self.package_license_comment_set = True
            if validate_pkg_lics_comment(text):
                doc.package.license_comment = str_from_text(text)
                return True
            else:
                raise ValueError('Package::LicenseComment')
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
            if validate_pkg_cr_text(text):
                if type(text) is str:
                    doc.package.cr_text = str_from_text(text)
                else:
                    doc.package.cr_text = text  # None or NoAssert
            else:
                raise ValueError('Package::CopyrightText')
        else:
            raise CardinalityError('Package::CopyrightText')

    def set_pkg_summary(self, doc, text):
        """Set's the package summary.
        Raises ValueError if text is not free form text.
        Raises CardinalityError if summary already set.
        Raises OrderError if no package previously defined.
        """
        self.assert_package_exists()
        if not self.package_summary_set:
            self.package_summary_set = True
            if validate_pkg_summary(text):
                doc.package.summary = str_from_text(text)
            else:
                raise ValueError('Package::Summary')
        else:
            raise CardinalityError('Package::Summary')

    def set_pkg_desc(self, doc, text):
        """Set's the package's description.
        Raises ValueError if text is not free form text.
        Raises CardinalityError if description already set.
        Raises OrderError if no package previously defined.
        """
        self.assert_package_exists()
        if not self.package_desc_set:
            self.package_desc_set = True
            if validate_pkg_desc(text):
                doc.package.description = str_from_text(text)
            else:
                raise ValueError('Package::Description')
        else:
            raise CardinalityError('Package::Description')

    def assert_package_exists(self):
        if not self.package_set:
            raise OrderError('Package')


class FileBuilder(object):

    def __init__(self):
        super(FileBuilder, self).__init__()
        self.reset_file_stat()

    def set_file_name(self, doc, name):
        """Raises OrderError if no package defined.
        """
        if self.has_package(doc):
            doc.package.files.append(file.File(name))
            self.reset_file_stat()
            return True
        else:
            raise OrderError('File::Name')

    def set_file_comment(self, doc, text):
        """
        Raises OrderError if no package or no file defined.
        Raises CardinalityError if more than one comment set.
        Raises ValueError if text is not free form text.
        """
        if self.has_package(doc) and self.has_file(doc):
            if not self.file_comment_set:
                self.file_comment_set = True
                if validate_file_comment(text):
                    self.file(doc).comment = str_from_text(text)
                    return True
                else:
                    raise ValueError('File::Comment')
            else:
                raise CardinalityError('File::Comment')
        else:
            raise OrderError('File::Comment')

    def set_file_type(self, doc, type):
        """
        Raises OrderError if no package or file defined.
        Raises CardinalityError if more than one type set.
        Raises ValueError if type is unknown.
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
                if type in type_dict.keys():
                    self.file(doc).type = type_dict[type]
                    return True
                else:
                    raise ValueError('File::Type')
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
                self.file(doc).chk_sum = chksum
                return True
            else:
                raise CardinalityError('File::CheckSum')
        else:
            raise OrderError('File::CheckSum')

    def set_concluded_license(self, doc, license):
        """
        Raises OrderError if no package or file defined.
        Raises CardinalityError if already set.
        Raises ValueError if malformed.
        """
        if self.has_package(doc) and self.has_file(doc):
            if not self.file_conc_lics_set:
                self.file_conc_lics_set = True
                if validate_lics_conc(license):
                    self.file(doc).conc_lics = license
                    return True
                else:
                    raise ValueError('File::ConcludedLicense')
            else:
                raise CardinalityError('File::ConcludedLicense')
        else:
            raise OrderError('File::ConcludedLicense')

    def set_file_license_in_file(self, doc, license):
        """
        Raises OrderError if no package or file defined.
        Raises ValueError if malformed value.
        """
        if self.has_package(doc) and self.has_file(doc):
            if validate_file_lics_in_file(license):
                if ((license is None) or
                        (type(license) is utils.NoAssert)):
                    self.file(doc).licenses_in_file.append(license)
                    return True
                else:
                    self.file(doc).licenses_in_file.append(
                        document.License.from_identifier(license))
                    return True
            else:
                raise ValueError('File::LicenseInFile')
        else:
            raise OrderError('File::LicenseInFile')

    def set_file_license_comment(self, doc, text):
        """
        Raises OrderError if no package or file defined.
        Raises ValueError if text is not free form text.
        Raises CardinalityError if more than one per file.
        """
        if self.has_package(doc) and self.has_file(doc):
            if not self.file_license_comment_set:
                self.file_license_comment_set = True
                if validate_file_lics_comment(text):
                    self.file(doc).license_comment = str_from_text(text)
                else:
                    raise ValueError('File::LicenseComment')
            else:
                raise CardinalityError('File::LicenseComment')
        else:
            raise OrderError('File::LicenseComment')

    def set_file_copyright(self, doc, text):
        """Raises OrderError if no package or file defined.
        Raises ValueError if not free form text or NONE or NO_ASSERT.
        Raises CardinalityError if more than one.
        """
        if self.has_package(doc) and self.has_file(doc):
            if not self.file_copytext_set:
                self.file_copytext_set = True
                if validate_file_cpyright(text):
                    if type(text) is str:
                        self.file(doc).copyright = str_from_text(text)
                    else:
                        self.file(doc).copyright = text  # None or NoAssert

                    return True
                else:
                    raise ValueError('File::CopyRight')
            else:
                raise CardinalityError('File::CopyRight')
        else:
            raise OrderError('File::CopyRight')

    def set_file_notice(self, doc, text):
        """Raises OrderError if no package or file defined.
        Raises ValueError if not free form text.
        Raises CardinalityError if more than one.
        """
        if self.has_package(doc) and self.has_file(doc):
            if not self.file_notice_set:
                self.file_notice_set = True
                if validate_file_notice(text):
                    self.file(doc).notice = str_from_text(text)
                else:
                    raise ValueError('File::Notice')
            else:
                raise CardinalityError('File::Notice')
        else:
            raise OrderError('File::Notice')

    def add_file_contribution(self, doc, value):
        """Raises OrderError if no package or file defined.
        """
        if self.has_package(doc) and self.has_file(doc):
            self.file(doc).contributers.append(value)
        else:
            raise OrderError('File::Contributor')

    def add_file_dep(self, doc, value):
        """Raises OrderError if no package or file defined.
        """
        if self.has_package(doc) and self.has_file(doc):
            self.file(doc).dependencies.append(value)
        else:
            raise OrderError('File::Dependency')

    def set_file_artifact_of_project_name(self, doc, value):
        """Raises OrderError if no package or file defined.
        """
        if self.has_package(doc) and self.has_file(doc):
            self.file(doc).artifact_of_project_name.append(value)
        else:
            raise OrderError('File::AoFProfjectName')

    def set_file_artificat_of_project_home(self, doc, value):
        """Raises OrderError if no package or file defined.
        """
        if self.has_package(doc) and self.has_file(doc):
            self.file(doc).artifact_of_project_home.append(value)
        else:
            raise OrderError('File::AoFProfjectHome')

    def set_file_artificat_of_project_uri(self, doc, value):
        """Raises OrderError if no package or file defined.
        """
        if self.has_package(doc) and self.has_file(doc):
            self.file(doc).artifact_of_project_uri.append(value)
        else:
            raise OrderError('File::AoFProfjectUri')

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
        self.file_comment_set = False
        self.file_type_set = False
        self.file_chksum_set = False
        self.file_conc_lics_set = False
        self.file_license_comment_set = False
        self.file_notice_set = False


class LicenseBuilder(object):

    def __init__(self):
        super(LicenseBuilder, self).__init__()


class Builder(DocBuilder, CreationInfoBuilder, EntityBuilder, ReviewBuilder,
              PackageBuilder, FileBuilder, LicenseBuilder):

    """SPDX document builder."""

    def __init__(self):
        super(Builder, self).__init__()
