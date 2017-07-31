
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

from functools import total_ordering

from spdx import config


def _add_parens(required, text):
    """
    Add parens around a license expression if `required` is True, otherwise
    return `text` unmodified.
    """
    return '({})'.format(text) if required else text


@total_ordering
class License(object):
    def __init__(self, full_name, identifier):
        self._full_name = full_name
        self._identifier = identifier

    @classmethod
    def from_identifier(cls, identifier):
        """If identifier exists in config.LICENSE_MAP
        the full_name is retrieved from it. Otherwise
        the full_name is the same as the identifier.
        """
        if identifier in config.LICENSE_MAP.keys():
            return cls(config.LICENSE_MAP[identifier], identifier)
        else:
            return cls(identifier, identifier)

    @classmethod
    def from_full_name(cls, full_name):
        """
        Returna new License for a full_name. If the full_name exists in
        config.LICENSE_MAP the identifier is retrieved from it.
        Otherwise the identifier is the same as the full_name.
        """
        if full_name in config.LICENSE_MAP.keys():
            return cls(full_name, config.LICENSE_MAP[full_name])
        else:
            return cls(full_name, full_name)

    @property
    def url(self):
        return "http://spdx.org/licenses/{0}".format(self.identifier)

    @property
    def full_name(self):
        return self._full_name

    @full_name.setter
    def full_name(self, value):
        self._full_name = value

    @property
    def identifier(self):
        return self._identifier

    def __eq__(self, other):
        return (
            isinstance(other, License)
            and self.identifier == other.identifier
            and self.full_name == other.full_name)

    def __lt__(self, other):
        return isinstance(other, License) and self.identifier < other.identifier

    def __str__(self):
        return self.identifier

    def __hash__(self):
        return self.identifier.__hash__()


class LicenseConjunction(License):
    """
    A conjunction of two licenses.
    """

    def __init__(self, license_1, license_2):
        self.license_1 = license_1
        self.license_2 = license_2
        super(LicenseConjunction, self).__init__(self.full_name, self.identifier)

    @property
    def full_name(self):
        license_1_complex = type(self.license_1) == LicenseDisjunction
        license_2_complex = type(self.license_2) == LicenseDisjunction

        return '{0} AND {1}'.format(
            _add_parens(license_1_complex, self.license_1.full_name),
            _add_parens(license_2_complex, self.license_2.full_name))

    @property
    def identifier(self):
        license_1_complex = type(self.license_1) == LicenseDisjunction
        license_2_complex = type(self.license_2) == LicenseDisjunction

        return '{0} AND {1}'.format(
            _add_parens(license_1_complex, self.license_1.identifier),
            _add_parens(license_2_complex, self.license_2.identifier))


class LicenseDisjunction(License):
    """
    A disjunction of two licenses.
    """

    def __init__(self, license_1, license_2):
        self.license_1 = license_1
        self.license_2 = license_2
        super(LicenseDisjunction, self).__init__(self.full_name, self.identifier)

    @property
    def full_name(self):
        license_1_complex = type(self.license_1) == LicenseConjunction
        license_2_complex = type(self.license_2) == LicenseConjunction

        return '{0} OR {1}'.format(
            _add_parens(license_1_complex, self.license_1.full_name),
            _add_parens(license_2_complex, self.license_2.full_name))

    @property
    def identifier(self):
        license_1_complex = type(self.license_1) == LicenseConjunction
        license_2_complex = type(self.license_2) == LicenseConjunction

        return '{0} OR {1}'.format(
            _add_parens(license_1_complex, self.license_1.identifier),
            _add_parens(license_2_complex, self.license_2.identifier))


@total_ordering
class ExtractedLicense(License):
    """
    Represent an ExtractedLicense with its additional attributes:
    - text: Extracted text, str. Mandatory.
    - cross_ref: list of cross references.
    - comment: license comment, str.
    - full_name: license name. str or utils.NoAssert.
    """
    def __init__(self, identifier):
        super(ExtractedLicense, self).__init__(None, identifier)
        self.text = None
        self.cross_ref = []
        self.comment = None

    def __eq__(self, other):
        return (
            isinstance(other, ExtractedLicense)
            and self.identifier == other.identifier
            and self.full_name == other.full_name)

    def __lt__(self, other):
        return isinstance(other, ExtractedLicense) and self.identifier < other.identifier

    def add_xref(self, ref):
        self.cross_ref.append(ref)

    def validate(self, messages=None):
        # FIXME: messages should be returned
        messages = messages if messages is not None else []

        if self.text is None:
            messages.append('ExtractedLicense text can not be None')
            return False
        else:
            return True


class Document(object):
    """
    Represent an SPDX document with these fields:
    - version: Spec version. Mandatory, one - Type: Version.
    - data_license: SPDX-Metadata license. Mandatory, one. Type: License.
    - comment: Comments on the SPDX file, optional one. Type: str
    - creation_info: SPDX file creation info. Mandatory, one. Type: CreationInfo
    - package: Package described by this document. Mandatory, one. Type: Package
    - extracted_licenses: List of licenses extracted that are not part of the
      SPDX license list. Optional, many. Type: ExtractedLicense.
    - reviews: SPDX document review information, Optional zero or more.
      Type: Review.
    """

    def __init__(self, version=None, data_license=None, comment=None, package=None):
        # avoid recursive impor
        from spdx.creationinfo import CreationInfo
        self.version = version
        self.data_license = data_license
        self.comment = comment
        self.creation_info = CreationInfo()
        self.package = package
        self.extracted_licenses = []
        self.reviews = []

    def add_review(self, review):
        self.reviews.append(review)

    def add_extr_lic(self, lic):
        self.extracted_licenses.append(lic)

    @property
    def files(self):
        return self.package.files

    @files.setter
    def files(self, value):
        self.package.files = value

    @property
    def has_comment(self):
        return self.comment is not None

    def validate(self, messages=None):
        """
        Validate all fields of the document and update the
        messages list with user friendly error messages for display.
        """
        # FIXME: messages should be returned
        messages = messages if messages is not None else []

        return (self.validate_version(messages)
            and self.validate_data_lics(messages)
            and self.validate_creation_info(messages)
            and self.validate_package(messages)
            and self.validate_extracted_licenses(messages)
            and self.validate_reviews(messages)
        )

    def validate_version(self, messages=None):
        # FIXME: messages should be returned
        messages = messages if messages is not None else []

        if self.version is None:
            messages.append('Document has no version.')
            return False
        else:
            return True

    def validate_data_lics(self, messages=None):
        # FIXME: messages should be returned
        messages = messages if messages is not None else []

        if self.data_license is None:
            messages.append('Document has no data license.')
            return False

        if self.data_license.identifier == 'CC0-1.0':
            return True
        else:
            # FIXME: REALLY? what if someone wants to use something else?
            messages.append('Document data license must be CC0-1.0.')
            return False

    def validate_reviews(self, messages=None):
        # FIXME: messages should be returned
        messages = messages if messages is not None else []

        valid = True
        for review in self.reviews:
            valid = review.validate(messages) and valid
        return valid

    def validate_creation_info(self, messages=None):
        # FIXME: messages should be returned
        messages = messages if messages is not None else []

        if self.creation_info is not None:
            return self.creation_info.validate(messages)
        else:
            messages.append('Document has no creation information.')
            return False

    def validate_package(self, messages=None):
        # FIXME: messages should be returned
        messages = messages if messages is not None else []

        if self.package is not None:
            return self.package.validate(messages)
        else:
            messages.append('Document has no package.')
            return False

    def validate_extracted_licenses(self, messages=None):
        # FIXME: messages should be returned
        messages = messages if messages is not None else []

        valid = True
        for lic in self.extracted_licenses:
            if isinstance(lic, ExtractedLicense):
                valid = lic.validate(messages) and valid
            else:
                messages.append(
                    'Document extracted licenses must be of type '
                    'spdx.document.ExtractedLicense and not ' + type(lic))
                valid = False
        return valid
