# Copyright (c) 2022 spdx contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from functools import total_ordering

from spdx import config


@total_ordering
class License(object):
    def __init__(self, full_name, identifier):
        """if one of the argument is None, we try to map as much as possible
        """
        self._full_name = None
        self._identifier = None
        self.set_full_name(full_name)
        self.set_identifier(identifier)

    @classmethod
    def from_identifier(cls, identifier):
        """If identifier exists in config.LICENSE_MAP
        the full_name is retrieved from it. Otherwise
        the full_name is the same as the identifier.
        """
        return cls(None, identifier)

    @classmethod
    def from_full_name(cls, full_name):
        """
        Return a new License for a full_name. If the full_name exists in
        config.LICENSE_MAP the identifier is retrieved from it.
        Otherwise the identifier is the same as the full_name.
        """
        return cls(full_name, None)

    @property
    def url(self):
        return "http://spdx.org/licenses/{0}".format(self.identifier)

    @property
    def full_name(self):
        return self._full_name

    @full_name.setter
    def full_name(self, value):
        self.set_full_name(value)

    def set_full_name(self, value):

        if value is None:
            return
        if self._identifier is None:
            if value in config.LICENSE_MAP:
                self._identifier = config.LICENSE_MAP[value]
            else:
                self._identifier = value
        self._full_name = value

    @property
    def identifier(self):
        return self._identifier

    @identifier.setter
    def identifier(self, value):
        self.set_identifier(value)

    def set_identifier(self, value):
        if value is None:
            return
        if self._full_name is None:
            if value in config.LICENSE_MAP:
                self._full_name = config.LICENSE_MAP[value]
            else:
                self._full_name = value

        self._identifier = value


    def __eq__(self, other):
        return (
            isinstance(other, License)
            and self.identifier == other.identifier
            and self.full_name == other.full_name
        )

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

        return "{0} AND {1}".format(
            _add_parens(license_1_complex, self.license_1.full_name),
            _add_parens(license_2_complex, self.license_2.full_name),
        )

    @property
    def identifier(self):
        license_1_complex = type(self.license_1) == LicenseDisjunction
        license_2_complex = type(self.license_2) == LicenseDisjunction

        return "{0} AND {1}".format(
            _add_parens(license_1_complex, self.license_1.identifier),
            _add_parens(license_2_complex, self.license_2.identifier),
        )


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

        return "{0} OR {1}".format(
            _add_parens(license_1_complex, self.license_1.full_name),
            _add_parens(license_2_complex, self.license_2.full_name),
        )

    @property
    def identifier(self):
        license_1_complex = type(self.license_1) == LicenseConjunction
        license_2_complex = type(self.license_2) == LicenseConjunction

        return "{0} OR {1}".format(
            _add_parens(license_1_complex, self.license_1.identifier),
            _add_parens(license_2_complex, self.license_2.identifier),
        )


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
            and self.full_name == other.full_name
        )

    def __lt__(self, other):
        return (
            isinstance(other, ExtractedLicense) and self.identifier < other.identifier
        )

    def add_xref(self, ref):
        self.cross_ref.append(ref)

    def validate(self, messages):
        if self.text is None:
            messages.append("ExtractedLicense text can not be None")


def _add_parens(required, text):
    """
    Add parens around a license expression if `required` is True, otherwise
    return `text` unmodified.
    """
    return "({})".format(text) if required else text
