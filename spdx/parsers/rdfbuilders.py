
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

from spdx import checksum
from spdx import document
from spdx import version
from spdx.parsers.builderexceptions import CardinalityError
from spdx.parsers.builderexceptions import IncompatibleVersionError
from spdx.parsers.builderexceptions import OrderError
from spdx.parsers.builderexceptions import SPDXValueError
from spdx.parsers import tagvaluebuilders


class DocBuilder(object):
    VERS_STR_REGEX = re.compile(r'SPDX-(\d+)\.(\d+)', re.UNICODE)
    def __init__(self):
        super(DocBuilder, self).__init__()
        self.reset_document()

    def set_doc_version(self, doc, value):
        """Sets the document version.
        Raises value error if malformed value, CardinalityError
        if already defined, IncompatibleVersionError if not 1.2.
        """
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

    def set_doc_data_lic(self, doc, res):
        """Sets the document data license.
        Raises value error if malformed value, CardinalityError
        if already defined.
        """
        if not self.doc_data_lics_set:
            self.doc_data_lics_set = True
            res_parts = res.split('/')
            if len(res_parts) != 0:
                identifier = res_parts[-1]
                doc.data_license = document.License.from_identifier(identifier)
            else:
                raise SPDXValueError('Document::License')
        else:
            raise CardinalityError('Document::License')

    def set_doc_comment(self, doc, comment):
        """Sets document comment, Raises CardinalityError if
        comment already set.
        """
        if not self.doc_comment_set:
            self.doc_comment_set = True
            doc.comment = comment
        else:
            raise CardinalityError('Document::Comment')

    def reset_document(self):
        """Resets the state to allow building new documents"""
        self.doc_version_set = False
        self.doc_comment_set = False
        self.doc_data_lics_set = False


class EntityBuilder(tagvaluebuilders.EntityBuilder):

    def create_entity(self, doc, value):
        if self.tool_re.match(value):
            return self.build_tool(doc, value)
        elif self.person_re.match(value):
            return self.build_person(doc, value)
        elif self.org_re.match(value):
            return self.build_org(doc, value)
        else:
            raise SPDXValueError('Entity')


class CreationInfoBuilder(tagvaluebuilders.CreationInfoBuilder):

    def set_creation_comment(self, doc, comment):
        """Sets creation comment, Raises CardinalityError if
        comment already set.
        Raises SPDXValueError if not free form text.
        """
        if not self.creation_comment_set:
            self.creation_comment_set = True
            doc.creation_info.comment = comment
            return True
        else:
            raise CardinalityError('CreationInfo::Comment')


class PackageBuilder(tagvaluebuilders.PackageBuilder):

    def set_pkg_chk_sum(self, doc, chk_sum):
        """Sets the package check sum, if not already set.
        chk_sum - A string
        Raises CardinalityError if already defined.
        Raises OrderError if no package previously defined.
        """
        self.assert_package_exists()
        if not self.package_chk_sum_set:
            self.package_chk_sum_set = True
            doc.package.check_sum = checksum.Algorithm('SHA1', chk_sum)
        else:
            raise CardinalityError('Package::CheckSum')

    def set_pkg_source_info(self, doc, text):
        """Sets the package's source information, if not already set.
        text - Free form text.
        Raises CardinalityError if already defined.
        Raises OrderError if no package previously defined.
        """
        self.assert_package_exists()
        if not self.package_source_info_set:
            self.package_source_info_set = True
            doc.package.source_info = text
            return True
        else:
            raise CardinalityError('Package::SourceInfo')

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
        else:
            raise CardinalityError('Package::VerificationCode')

    def set_pkg_excl_file(self, doc, filename):
        """Sets the package's verification code excluded file.
        Raises OrderError if no package previously defined.
        """
        self.assert_package_exists()
        doc.package.add_exc_file(filename)

    def set_pkg_license_comment(self, doc, text):
        """Sets the package's license comment.
        Raises OrderError if no package previously defined.
        Raises CardinalityError if already set.
        """
        self.assert_package_exists()
        if not self.package_license_comment_set:
            self.package_license_comment_set = True
            doc.package.license_comment = text
            return True
        else:
            raise CardinalityError('Package::LicenseComment')

    def set_pkg_cr_text(self, doc, text):
        """Sets the package's license comment.
        Raises OrderError if no package previously defined.
        Raises CardinalityError if already set.
        """
        self.assert_package_exists()
        if not self.package_cr_text_set:
            self.package_cr_text_set = True
            doc.package.cr_text = text
        else:
            raise CardinalityError('Package::CopyrightText')

    def set_pkg_summary(self, doc, text):
        """Set's the package summary.
        Raises CardinalityError if summary already set.
        Raises OrderError if no package previously defined.
        """
        self.assert_package_exists()
        if not self.package_summary_set:
            self.package_summary_set = True
            doc.package.summary = text
        else:
            raise CardinalityError('Package::Summary')

    def set_pkg_desc(self, doc, text):
        """Set's the package's description.
        Raises CardinalityError if description already set.
        Raises OrderError if no package previously defined.
        """
        self.assert_package_exists()
        if not self.package_desc_set:
            self.package_desc_set = True
            doc.package.description = text
        else:
            raise CardinalityError('Package::Description')


class FileBuilder(tagvaluebuilders.FileBuilder):

    def set_file_chksum(self, doc, chk_sum):
        """Sets the file check sum, if not already set.
        chk_sum - A string
        Raises CardinalityError if already defined.
        Raises OrderError if no package previously defined.
        """
        if self.has_package(doc) and self.has_file(doc):
            if not self.file_chksum_set:
                self.file_chksum_set = True
                self.file(doc).chk_sum = checksum.Algorithm('SHA1', chk_sum)
                return True
            else:
                raise CardinalityError('File::CheckSum')
        else:
            raise OrderError('File::CheckSum')

    def set_file_license_comment(self, doc, text):
        """
        Raises OrderError if no package or file defined.
        Raises CardinalityError if more than one per file.
        """
        if self.has_package(doc) and self.has_file(doc):
            if not self.file_license_comment_set:
                self.file_license_comment_set = True
                self.file(doc).license_comment = text
                return True
            else:
                raise CardinalityError('File::LicenseComment')
        else:
            raise OrderError('File::LicenseComment')

    def set_file_copyright(self, doc, text):
        """Raises OrderError if no package or file defined.
        Raises CardinalityError if more than one.
        """
        if self.has_package(doc) and self.has_file(doc):
            if not self.file_copytext_set:
                self.file_copytext_set = True
                self.file(doc).copyright = text
                return True
            else:
                raise CardinalityError('File::CopyRight')
        else:
            raise OrderError('File::CopyRight')

    def set_file_comment(self, doc, text):
        """Raises OrderError if no package or no file defined.
        Raises CardinalityError if more than one comment set.
        """
        if self.has_package(doc) and self.has_file(doc):
            if not self.file_comment_set:
                self.file_comment_set = True
                self.file(doc).comment = text
                return True
            else:
                raise CardinalityError('File::Comment')
        else:
            raise OrderError('File::Comment')

    def set_file_notice(self, doc, text):
        """Raises OrderError if no package or file defined.
        Raises CardinalityError if more than one.
        """
        if self.has_package(doc) and self.has_file(doc):
            if not self.file_notice_set:
                self.file_notice_set = True
                self.file(doc).notice = tagvaluebuilders.str_from_text(text)
                return True
            else:
                raise CardinalityError('File::Notice')
        else:
            raise OrderError('File::Notice')


class ReviewBuilder(tagvaluebuilders.ReviewBuilder):
    def add_review_comment(self, doc, comment):
        """Sets the review comment. Raises CardinalityError if
        already set. OrderError if no reviewer defined before.
        """
        if len(doc.reviews) != 0:
            if not self.review_comment_set:
                self.review_comment_set = True
                doc.reviews[-1].comment = comment
                return True
            else:
                raise CardinalityError('ReviewComment')
        else:
            raise OrderError('ReviewComment')


class Builder(DocBuilder, EntityBuilder, CreationInfoBuilder, PackageBuilder, FileBuilder, ReviewBuilder):

    def reset(self):
        """Resets builder's state for building new documents.
        Must be called between usage with different documents.
        """
        self.reset_document()
        self.reset_package()
        self.reset_file_stat()
        self.reset_reviews()
