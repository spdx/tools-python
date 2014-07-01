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

import checksum


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
        conc_lics: Mandatory spdx.document.License.
        license_declared : spdx.document.License.
        license_comment  : optional string.
        licenses_from_files: spdx.document.License.
        cr_text: Copyright text, string , NoAssertion or NONE. Mandatory.
        summary: Optional str.
        description: Optional str.
        files: List of files in package, atleast one.
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

    def add_file(self, file):
        self.files.append(file)

    def validate(self, messages):
        """Validates the package's fields. Appends user friends errors
        to messages.
        """
        value = (self.validate_checksum(messages) &
                 self.validate_optional_str_fields(messages) &
                 self.validate_mandatory_str_fields(messages)
                 & self.validate_files(messages))
        return value

    def validate_files(self, messages):
        if len(self.files) == 0:
            messages.append('Package must have at least one file.')
            return False
        else:
            return_value = True
            for f in self.files:
                return_value &= f.validate(messages)
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
        for field in fields:
            if field is not None:
                field = eval('self.{0}'.format(field))
                attr = getattr(field, '__str__', None)
                if not callable(attr):
                    messages.append('{0} must provide __str__ method.'.format(
                        field))
                    return_value = False  # Continue checking.
            elif not optional:
                messages.append('{0} can not be None.'.format(field))
                return_value = False

        return return_value

    def validate_checksum(self, messages):
        return (self.check_sum is None) or isinstance(self.check_sum,
                                                      checksum.Algorithm)


    def has_optional_field(self, field):
        expr = 'self.{0} is not None'.format(field)
        return eval(expr)
