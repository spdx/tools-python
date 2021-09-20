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

import hashlib

from functools import reduce

from spdx import checksum
from spdx import creationinfo
from spdx import document
from spdx import utils


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
     If set to "false", the package must not contain any files.
     Optional, boolean.
     - homepage: Optional, URL as string or NONE or NO_ASSERTION.
     - verif_code: string. Mandatory if files_analyzed is True or None (omitted)
       Must be None (omitted) if files_analyzed is False
     - check_sum: Optional , spdx.checksum.Algorithm.
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
     - files: List of files in package, atleast one.
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
        self.check_sum = None
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
        self.files = []
        self.verif_exc_files = []
        self.pkg_ext_refs = []

    @property
    def are_files_analyzed(self):
        return self.files_analyzed is not False
        # as default None Value is False, previous line is simplification of
        # return self.files_analyzed or self.files_analyzed is None

    def add_file(self, fil):
        self.files.append(fil)

    def add_lics_from_file(self, lics):
        self.licenses_from_files.append(lics)

    def add_exc_file(self, filename):
        self.verif_exc_files.append(filename)

    def add_pkg_ext_refs(self, pkg_ext_ref):
        self.pkg_ext_refs.append(pkg_ext_ref)

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
        self.validate_files(messages)
        self.validate_pkg_ext_refs(messages)
        self.validate_mandatory_fields(messages)
        self.validate_optional_fields(messages)
        messages.pop_context()

        return messages

    def validate_files_analyzed(self, messages):
        if self.files_analyzed not in [ True, False, None ]:
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

    def validate_pkg_ext_refs(self, messages):
        for ref in self.pkg_ext_refs:
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

    def validate_files(self, messages):
        if self.are_files_analyzed:
            if not self.files:
                messages.append(
                    "Package must have at least one file."
                )
            else:
                for f in self.files:
                    messages = f.validate(messages)

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
        FIELDS = ["name", "spdx_id", "download_location", "cr_text"]
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
                messages.append("Package {0} can not be None.".format(field_str))

        return messages

    def validate_checksum(self, messages):
        if self.check_sum is not None:
            if not isinstance(self.check_sum, checksum.Algorithm):
                messages.append(
                    "Package checksum must be instance of spdx.checksum.Algorithm"
                )

        return messages

    def calc_verif_code(self):
        hashes = []

        for file_entry in self.files:
            if (
                isinstance(file_entry.chk_sum, checksum.Algorithm)
                and file_entry.chk_sum.identifier == "SHA1"
            ):
                sha1 = file_entry.chk_sum.value
            else:
                sha1 = file_entry.calc_chksum()
            hashes.append(sha1)

        hashes.sort()

        sha1 = hashlib.sha1()
        sha1.update("".join(hashes).encode("utf-8"))
        return sha1.hexdigest()

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
