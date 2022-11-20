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

import enum
import hashlib

from functools import reduce

from spdx import checksum
from spdx import creationinfo
from spdx import document
from spdx import utils


class PackagePrimaryPurpose(enum.IntEnum):
    APPLICATION = 1
    FRAMEWORK = 2
    LIBRARY = 3
    CONTAINER = 4
    OPERATINGSYSTEM = 5
    DEVICE = 6
    FIRMWARE = 7
    SOURCE = 8
    ARCHIVE = 9
    FILE = 10
    INSTALL = 11
    OTHER = 12

    @classmethod
    def by_name(cls, lookup):
        if lookup.lower() == 'operating-system':
            lookup = 'operatingsystem'
        return PackagePrimaryPurpose.__getitem__(lookup)


PKG_PURPOSE_TO_XML_DICT = {}
PKG_PURPOSE_FROM_XML_DICT = {}
for ppp in list(PackagePrimaryPurpose):
    name = ppp.name.lower()
    if name == 'operatingsystem':  # so this is a little weird.
        name = 'operating-system'
    xml_name = 'packagePurpose_{}'.format(ppp.name.lower())
    PKG_PURPOSE_TO_XML_DICT[ppp] = xml_name
    PKG_PURPOSE_FROM_XML_DICT[xml_name] = ppp


class Package(object):

    """
    Represent an analyzed Package.
    Fields:
     - name : Mandatory, string.
     - spdx_id: Uniquely identify any element in an SPDX document which may be
     referenced by other elements. Mandatory, one. Type: str.
     - version: Optional, string.
     - file_name: Optional, string.
     - supplier: Optional, Organization or Person or NO_ASSERTION.
     - originator: Optional, Organization or Person.
     - download_location: Mandatory, URL as string.
     - files_analyzed: Indicates whether the file content of this package has
     been available for or subjected to analysis when creating the SPDX
     document. If "false" indicates packages that represent metadata or URI
     references to a project, product, artifact, distribution or a component.
     If set to "false", the package must not contain any has_files.
     Optional, boolean.
     - homepage: Optional, URL as string or NONE or NO_ASSERTION.
     - verif_code: string. Mandatory if files_analyzed is True or None (omitted)
       Must be None (omitted) if files_analyzed is False
     - checksums: Optional, dict of values keyed by algorithm name
     - source_info: Optional string.
     - conc_lics: Mandatory spdx.document.License or spdx.utils.SPDXNone or
     - spdx.utils.NoAssert.
     - license_declared : Mandatory spdx.document.License or spdx.utils.SPDXNone or
     - spdx.utils.NoAssert.
     - license_comment  : optional string.
     - licenses_from_files: list of spdx.document.License or spdx.utils.SPDXNone or
     - spdx.utils.NoAssert.
     - cr_text: Copyright text, string , utils.NoAssert or utils.SPDXNone. Mandatory.
     - summary: Optional str.
     - description: Optional str.
     - comment: Comments about the package being described, optional one.
     Type: str
     - has_files: List SPDXIDs of files in package, 0..n or missing
     - verif_exc_files : list of file names excluded from verification code or None.
     - ext_pkg_refs : External references referenced within the given package.
     Optional, one or many. Type: ExternalPackageRef
     - attribution_text : optional string.
    """

    def __init__(
        self,
        name=None,
        spdx_id=None,
        download_location=None,
        version=None,
        file_name=None,
        supplier=None,
        originator=None,
    ):
        self.name = name
        self.spdx_id = spdx_id
        self.version = version
        self.file_name = file_name
        self.supplier = supplier
        self.originator = originator
        self.download_location = download_location
        self.files_analyzed = None
        self.homepage = None
        self.verif_code = None
        self.checksums = {}
        self.source_info = None
        self.conc_lics = None
        self.license_declared = None
        self.license_comment = None
        self.licenses_from_files = []
        self.cr_text = None
        self.summary = None
        self.description = None
        self.comment = None
        self.attribution_text = None
        self.has_files = []
        self.verif_exc_files = []
        self.external_references = []
        self.annotations = []
        self.primary_purpose = []
        self.built_date = None
        self.release_date = None
        self.valid_until_date = None

    @property
    def check_sum(self):
        """
        Backwards compatibility, return first checksum.
        deprecated, use get_checksum()
        """
        return self.get_checksum('SHA1')

    @check_sum.setter
    def check_sum(self, value):
        if isinstance(value, str):
            self.set_checksum(checksum.Algorithm('SHA1', value))
        elif isinstance(value, checksum.Algorithm):
            self.set_checksum(value)
        else:
            raise ValueError('cannot call check_sum with value of type {}.'.format(type(value)))

    @property
    def are_files_analyzed(self):
        if self.files_analyzed is None:
            return True  # default is True
        else:
            return self.files_analyzed

    def add_lics_from_file(self, lics):
        self.licenses_from_files.append(lics)

    def add_exc_file(self, filename):
        self.verif_exc_files.append(filename)

    def add_external_references(self, pkg_ext_ref):
        if isinstance(pkg_ext_ref, ExternalPackageRef):
            self.external_references.append(pkg_ext_ref)
        else:
            raise ValueError('cannot add external reference of type {}'.format(type(pkg_ext_ref)))

    def validate(self, messages):
        """
        Validate the package fields.
        Append user friendly error messages to the `messages` list.
        """
        messages.push_context(self.name)
        self.validate_files_analyzed(messages)
        self.validate_checksum(messages)
        self.validate_optional_str_fields(messages)
        self.validate_mandatory_str_fields(messages)
        self.validate_has_files(messages)
        self.validate_external_references(messages)
        self.validate_mandatory_fields(messages)
        self.validate_optional_fields(messages)
        messages.pop_context()

        return messages

    def validate_files_analyzed(self, messages):
        if self.files_analyzed not in [True, False, None]:
            messages.append(
                'Package files_analyzed must be True or False or None (omitted)'
            )
        if not self.are_files_analyzed and self.verif_code is not None:
            messages.append(
                'Package verif_code must be None (omitted) when files_analyzed is False'
            )

        return messages

    def validate_optional_fields(self, messages):
        if self.originator and not isinstance(
            self.originator, (utils.NoAssert, creationinfo.Creator)
        ):
            messages.append(
                "Package originator must be instance of "
                "spdx.utils.NoAssert or spdx.creationinfo.Creator"
            )

        if self.supplier and not isinstance(
            self.supplier, (utils.NoAssert, creationinfo.Creator)
        ):
            messages.append(
                "Package supplier must be instance of "
                "spdx.utils.NoAssert or spdx.creationinfo.Creator"
            )

        return messages

    def validate_external_references(self, messages):
        for ref in self.external_references:
            if isinstance(ref, ExternalPackageRef):
                messages = ref.validate(messages)
            else:
                messages.append(
                    "External package references must be of the type "
                    "spdx.package.ExternalPackageRef and not " + str(type(ref))
                )

        return messages

    def validate_mandatory_fields(self, messages):
        if not isinstance(
            self.conc_lics, (utils.SPDXNone, utils.NoAssert, document.License)
        ):
            messages.append(
                "Package concluded license must be instance of "
                "spdx.utils.SPDXNone or spdx.utils.NoAssert or "
                "spdx.document.License"
            )

        if not isinstance(
            self.license_declared, (utils.SPDXNone, utils.NoAssert, document.License)
        ):
            messages.append(
                "Package declared license must be instance of "
                "spdx.utils.SPDXNone or spdx.utils.NoAssert or "
                "spdx.document.License"
            )

        # FIXME: this is obscure and unreadable
        license_from_file_check = lambda prev, el: prev and isinstance(
            el, (document.License, utils.SPDXNone, utils.NoAssert)
        )
        if not reduce(license_from_file_check, self.licenses_from_files, True):
            messages.append(
                "Each element in licenses_from_files must be instance of "
                "spdx.utils.SPDXNone or spdx.utils.NoAssert or "
                "spdx.document.License"
            )

        if not self.licenses_from_files and self.are_files_analyzed:
            messages.append("Package licenses_from_files can not be empty")

        return messages

    def validate_has_files(self, messages):
        if self.are_files_analyzed:
            if self.has_files is None or len(self.has_files) == 0:
                messages.append('Package must have at least one has_file.')
        return messages

    def validate_optional_str_fields(self, messages):
        """Fields marked as optional and of type string in class
        docstring must be of a type that provides __str__ method.
        """
        FIELDS = [
            "file_name",
            "version",
            "homepage",
            "source_info",
            "summary",
            "description",
            "attribution_text",
            "comment",
        ]
        self.validate_str_fields(FIELDS, True, messages)

        return messages

    def validate_mandatory_str_fields(self, messages):
        """Fields marked as Mandatory and of type string in class
        docstring must be of a type that provides __str__ method.
        """
        FIELDS = ["name", "spdx_id", "download_location"]
        if self.are_files_analyzed:
            FIELDS = FIELDS + ["verif_code"]
        self.validate_str_fields(FIELDS, False, messages)

        return messages

    def validate_str_fields(self, fields, optional, messages):
        """Helper for validate_mandatory_str_field and
        validate_optional_str_fields"""
        for field_str in fields:
            field = getattr(self, field_str)
            if field is not None:
                # FIXME: this does not make sense???
                attr = getattr(field, "__str__", None)
                if not callable(attr):
                    messages.append(
                        "{0} must provide __str__ method.".format(field)
                    )
                    # Continue checking.
            elif not optional:
                pass
                messages.append("Package {0} can not be None.".format(field_str))

        return messages

    def validate_checksum(self, messages):
        if self.checksums is not None and len(self.checksums) > 0:
            found_sha1 = False
            for algo, value in self.checksums.items():
                if algo not in checksum.CHECKSUM_ALGORITHMS:
                    messages.append('Unknown package checksum algorithm {}'.format(algo))
                if algo == 'SHA1':
                    found_sha1 = True
            if not found_sha1:
                messages.append('At least one package checksum algorithm must be SHA1')
        return messages

    def calc_verif_code(self, document):
        """
        calculate the new package hash code using related document
        """
        list_of_file_hashes = []
        hash_algo_name = "SHA1"
        for spdx_id in self.has_files:
            for f in document.files:
                if f.spdx_id == spdx_id:
                    file_chksum = f.get_checksum(hash_algo_name)
                    if file_chksum is not None:
                        file_ch = file_chksum.value
                    else:
                        file_ch = f.calculate_checksum(hash_algo_name)
                    list_of_file_hashes.append(file_ch)

        list_of_file_hashes.sort()

        hasher = hashlib.new(hash_algo_name.lower())
        hasher.update("".join(list_of_file_hashes).encode("utf-8"))
        return hasher.hexdigest()

    def get_checksum(self, hash_algorithm='SHA1'):
        if hash_algorithm not in checksum.CHECKSUM_ALGORITHMS:
            raise ValueError('checksum algorithm {} is not supported'.format(hash_algorithm))
        value = self.checksums.get(hash_algorithm)
        if value is not None:
            return checksum.Algorithm(hash_algorithm, value)
        else:
            return None

    def set_checksum(self, chk_sum):
        if isinstance(chk_sum, checksum.Algorithm):
            if chk_sum.identifier not in checksum.CHECKSUM_ALGORITHMS:
                raise ValueError('checksum algorithm {} is not supported'.format(chk_sum.identifier))
            self.checksums[chk_sum.identifier] = chk_sum.value
        else:
            raise ValueError('unknown chk_sum object type {}'.format(type(chk_sum)))

    def has_optional_field(self, field):
        return getattr(self, field, None) is not None


class ExternalPackageRef(object):
    """
    An External Reference allows a Package to reference an external source of
    additional information, metadata, enumerations, asset identifiers, or
    downloadable content believed to be relevant to the Package.
    Fields:
    - category: "SECURITY" or "PACKAGE-MANAGER" or "OTHER".
    - pkg_ext_ref_type: A unique string containing letters, numbers, ".","-".
    - locator: A unique string with no spaces necessary to access the
    package-specific information, metadata, or content within the target
    location.
    - comment: To provide information about the purpose and target of the
    reference.
    """

    def __init__(
        self, category=None, pkg_ext_ref_type=None, locator=None, comment=None
    ):
        self.category = category
        self.pkg_ext_ref_type = pkg_ext_ref_type
        self.locator = locator
        self.comment = comment

    def validate(self, messages):
        """
        Check that all the fields are valid.
        Appends any error messages to messages parameter shall be a ErrorMessages.
        """
        self.validate_category(messages)
        self.validate_pkg_ext_ref_type(messages)
        self.validate_locator(messages)

        return messages

    def validate_category(self, messages):
        if self.category is None:
            messages.append("ExternalPackageRef has no category.")

        return messages

    def validate_pkg_ext_ref_type(self, messages):
        if self.pkg_ext_ref_type is None:
            messages.append("ExternalPackageRef has no type.")

        return messages

    def validate_locator(self, messages):
        if self.locator is None:
            messages.append("ExternalPackageRef has no locator.")

        return messages
