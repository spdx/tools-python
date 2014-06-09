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
        return cls(config.LICENSE_MAP[identifier], identifier)

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
        files: List of files referenced by this SPDX document. atleast one mandatory.
        reviews: SPDX document review information, Optional zero or more. 
            Type: Review.
    """
    def __init__(self, version, data_license, comment=None, 
                creation_info=CreationInfo(), package=None):
        super(Document, self).__init__()
        self.version = version
        self.data_license = data_license
        self.comment = comment
        self.creation_info = creation_info
        self.package = package
        self.extracted_licenses = []
        self.reviews = []