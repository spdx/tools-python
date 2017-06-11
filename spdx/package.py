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

import hashlib

from six.moves import reduce

from spdx import checksum
from spdx import creationinfo
from spdx import document
from spdx import utils


class Package(object):

    """Represents an analyzed Package.
    Fields:
        name : Mandatory, string.
        version: Optional, string.
        file_name: Optional, string.
        supplier: Optional, Organization or Person or NO_ASSERTION.
        originator: Optional, Organization or Person.
        download_location: Mandatory, URL as string.
        homepage: Optional, URL as string or NONE or NO_ASSERTION.
        verif_code: Mandatory string.
        check_sum: Optional , spdx.checksum.Algorithm.
        source_info: Optional string.
        conc_lics: Mandatory spdx.document.License or spdx.utils.SPDXNone or
        spdx.utils.NoAssert.
        license_declared : Mandatory spdx.document.License or spdx.utils.SPDXNone or
        spdx.utils.NoAssert.
        license_comment  : optional string.
        licenses_from_files: list of spdx.document.License or spdx.utils.SPDXNone or
        spdx.utils.NoAssert.
        cr_text: Copyright text, string , utils.NoAssert or utils.SPDXNone. Mandatory.
        summary: Optional str.
        description: Optional str.
        files: List of files in package, atleast one.
        verif_exc_files : list of file names excluded from verification code or None.
    """

    def __init__(self, name=None, download_location=None, version=None,
                 file_name=None, supplier=None, originator=None):
        super(Package, self).__init__()
        self.name = name
        self.version = version
        self.file_name = file_name
        self.supplier = supplier
        self.originator = originator
        self.download_location = download_location
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
        self.files = []
        self.verif_exc_files = []

    def add_file(self, fil):
        self.files.append(fil)

    def add_lics_from_file(self, lics):
        self.licenses_from_files.append(lics)

    def add_exc_file(self, filename):
        self.verif_exc_files.append(filename)

    def validate(self, messages):
        """Validates the package's fields. Appends user friends errors
        to messages.
        """
        return (self.validate_checksum(messages) and
                self.validate_optional_str_fields(messages) and
                self.validate_mandatory_str_fields(messages) and
                self.validate_files(messages) and
                self.validate_mandatory_fields(messages) and
                self.validate_optional_fields(messages))

    def validate_optional_fields(self, messages):
        status = True

        if self.originator and not isinstance(self.originator, (utils.NoAssert, creationinfo.Creator)):
            messages.append('Package originator must be instance of ' +
                            'spdx.utils.NoAssert or spdx.creationinfo.Creator')
            status = False

        if self.supplier and not isinstance(self.supplier, (utils.NoAssert, creationinfo.Creator)):
            messages.append('Package supplier must be instance of ' +
                            'spdx.utils.NoAssert or spdx.creationinfo.Creator')
            status = False

        return status

    def validate_mandatory_fields(self, messages):
        status = True

        if not isinstance(self.conc_lics, (utils.SPDXNone, utils.NoAssert, document.License)):
            messages.append('Package concluded license must be instance of ' +
                            'spdx.utils.SPDXNone or spdx.utils.NoAssert or spdx.document.License')
            status = False

        if not isinstance(self.license_declared, (utils.SPDXNone, utils.NoAssert, document.License)):
            messages.append('Package declared license must be instance of ' +
                            'spdx.utils.SPDXNone or spdx.utils.NoAssert or spdx.document.License')
            status = False

        license_from_file_check = lambda prev, el: \
            prev and isinstance(el, (document.License, utils.SPDXNone, utils.NoAssert))

        if not reduce(license_from_file_check, self.licenses_from_files, True):
            messages.append('each element in licenses_from_files must be instance of ' +
                            'spdx.utils.SPDXNone or spdx.utils.NoAssert or spdx.document.License')
            status = False

        if len(self.licenses_from_files) == 0:
            messages.append('Package licenses_from_files can not be empty')
            status = False

        return status

    def validate_files(self, messages):
        if len(self.files) == 0:
            messages.append('Package must have at least one file.')
            return False
        else:
            return_value = True
            for f in self.files:
                return_value = return_value and f.validate(messages)
            return return_value

    def validate_optional_str_fields(self, messages):
        """Fields marked as optional and of type string in class
        docstring must be of a type that provides __str__ method.
        """
        FIELDS = ['file_name', 'version', 'homepage', 'source_info',
                  'summary', 'description']
        return self.validate_str_fields(FIELDS, True, messages)

    def validate_mandatory_str_fields(self, messages):
        """Fields marked as Mandatory and of type string in class
        docstring must be of a type that provides __str__ method.
        """
        FIELDS = ['name', 'download_location', 'verif_code', 'cr_text']
        return self.validate_str_fields(FIELDS, False, messages)

    def validate_str_fields(self, fields, optional, messages):
        """Helper for validate_mandatory_str_field and
        validate_optional_str_fields"""
        return_value = True
        for field_str in fields:
            field = eval('self.{0}'.format(field_str))
            if field is not None:
                attr = getattr(field, '__str__', None)
                if not callable(attr):
                    messages.append('{0} must provide __str__ method.'.format(
                        field))
                    return_value = False  # Continue checking.
            elif not optional:
                messages.append('Package {0} can not be None.'.format(field_str))
                return_value = False

        return return_value

    def validate_checksum(self, messages):
        if self.check_sum is None:
            return True
        elif isinstance(self.check_sum, checksum.Algorithm):
            if self.check_sum.identifier == 'SHA1':
                return True
            else:
                messages.append('File checksum algorithm must be SHA1')
                return False
        else:
            messages.append('Package checksum must be instance of spdx.checksum.Algorithm')
            return False

    def calc_verif_code(self):
        hashes = []

        for file_entry in self.files:
            if (isinstance(file_entry.chk_sum, checksum.Algorithm) and
                file_entry.chk_sum.identifier == 'SHA1'):
                sha1 = file_entry.chk_sum.value
            else:
                sha1 = file_entry.calc_chksum()
            hashes.append(sha1)

        hashes.sort()

        sha1 = hashlib.sha1()
        sha1.update(''.join(hashes))
        return sha1.hexdigest()

    def has_optional_field(self, field):
        expr = 'self.{0} is not None'.format(field)
        return eval(expr)
