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


class Package(object):

    """Represents an analyzed Package.
    Fields:
        name : Mandatory, string.
        version: Optional, string.
        file_name: Optional, string.
        supplier: Optional, Organization or Person or NO_ASSERTION.
        originator: Optional, Organization or Person.
        download_location: Mandatory, URL as string.
        homepage: Optional, URL as string or None or NO_ASSERTION.
        verif_code: Mandatory string.
        check_sum: Optional string.
        source_info: Optional string.
        conc_lists: Mandatory string.
        licenses_from_files: License list, at least one.
        cr_text: Copyright text, string , NoAssertion or None. Mandatory.
        summary: Optional str.
        description: Optional str.
        files: List of files in package, atleast one.
    """

    def __init__(self, name=None, download_location=None, version="", file_name="",
                 supplier=None, originator=None):
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

    def validate(self, messages):
        """Validates the package's fields. Appends user friends errors
        to messages.
        """
        return True
