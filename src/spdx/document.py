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
class Version(object):
    """Spec version, has Major and Minor number"""
    def __init__(self, major=1, minor=2):
        super(Version, self).__init__()
        self.major = major
        self.minor = minor
    def __cmp__(self, other):
        if self.major == other.major:
            return self.minor - other.minor
        elif self.major < other.major:
            return -1
        else:
            return 1


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
    """Represents an SPDX document."""
    def __init__(self, version, data_license, comment=None, 
                creation_info=CreationInfo(), package=None):
        super(Document, self).__init__()
        self.version = version
        self.data_license = data_license
        self.comment = comment
        self.creation_info = creation_info
        self.package = package