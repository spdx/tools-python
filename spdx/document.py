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
import config
from version import Version
from creationinfo import CreationInfo
from package import Package


class License(object):

    """Represents a License."""

    def __init__(self, full_name, identifier):
        super(License, self).__init__()
        self._full_name = full_name
        self._identifier = identifier

    @classmethod
    def from_identifier(cls, identifier):
        if identifier in config.LICENSE_MAP.keys():
            return cls(config.LICENSE_MAP[identifier], identifier)
        else:
            return cls(identifier, identifier)

    @classmethod
    def from_full_name(cls, full_name):
        return cls(full_name, config.LICENSE_MAP[full_name])

    @property
    def url(self):
        return "http://spdx.org/licenses/{0}".format(self.identifier)

    @property
    def full_name(self):
        return self._full_name

    @property
    def identifier(self):
        return self._identifier

    def __eq__(self, other):
        if isinstance(other, License):
            return ((self.identifier == other.identifier) &
                    (self.full_name == other.full_name))
        else:
            return False


class LicenseConjuction(License):

    """A conjuction of two licenses."""

    def __init__(self, license_1, license_2):
        self.license_1 = license_1
        self.license_2 = license_2
        super(LicenseConjuction, self).__init__(
            self.full_name, self.identifier)

    @property
    def full_name(self):
        return '{0} and {1}'.format(self.license_1.full_name,
                                    self.license_2.full_name)

    @property
    def identifier(self):
        return '{0} and {1}'.format(self.license_1.identifier,
                                    self.license_2.identifier)


class LicenseDisjunction(License):

    """A disjunction of two licenses."""

    def __init__(self, license_1, license_2):
        self.license_1 = license_1
        self.license_2 = license_2
        super(LicenseDisjunction, self).__init__(
            self.full_name, self.identifier)

    @property
    def full_name(self):
        return '{0} or {1}'.format(self.license_1.full_name,
                                   self.license_2.full_name)

    @property
    def identifier(self):
        return '{0} or {1}'.format(self.license_1.identifier,
                                   self.license_2.identifier)


class Document(object):

    """Represents an SPDX document.
        Fields: 
        version: Spec version. Mandatory, one - Type: Version.
        data_license: SPDX-Metadata license. Mandatory, one. Type: License.
        comment: Comments on the SPDX file, optional one. Type: str
        creation_info: SPDX file creation info. Mandatory, one. Type: CreationInfo
        package: Package described by this document. Mandatory, one. Type: Package
        extracted_licenses: List of licenses extracted that are not part of the
            SPDX license list. Optional, many. Type: License.
        reviews: SPDX document review information, Optional zero or more. 
            Type: Review.
    """

    def __init__(self, version=None, data_license=None, comment=None,
                 package=None):
        super(Document, self).__init__()
        self.version = version
        self.data_license = data_license
        self.comment = comment
        self.creation_info = CreationInfo()
        self.package = package
        self.extracted_licenses = []
        self.reviews = []

    def add_review(self, review):
        self.reviews.append(review)

    def validate(self, messages=[]):
        return (self.validate_version(messages)
                & self.validate_data_lics(messages)
                & self.validate_creation_info(messages)
                & self.validate_package(messages)
                & self.validate_extracted_licenses(messages)
                & self.validate_reviews(messages))

    def validate_version(self, messages):
        if self.version is not None:
            if self.version == Version(1, 2):
                return True
            else:
                messages.append('SPDX Version must be 1.2')
                return False
        else:
            messages.append('Document has no version.')
            return False

    def validate_data_lics(self, messages):
        if self.data_license is not None:
            if self.data_license.identifier == 'CC-1.0':
                return True
            else:
                messages.append('Document data license must be CC-1.0.')
                return False
        else:
            messages.append('Document has no data license.')
            return False

    def validate_reviews(self, messages):
        status = True
        for review in self.reviews:
            status &= review.validate(messages)
        return status

    def validate_creation_info(self, messages):
        if self.creation_info is not None:
            return self.creation_info.validate(messages)
        else:
            messages.append('Document has no creation information.')
            return False

    def validate_package(self, messages):
        if self.package is not None:
            return self.package.validate(messages)
        else:
            messages.append('Document has no package.')
            return False

    def validate_extracted_licenses(self, messages):
        return True  # TODO: Implement.
