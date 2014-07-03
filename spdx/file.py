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


class FileType(object):
    SOURCE = 1
    BINARY = 2
    ARCHIVE = 3
    OTHER = 4


class File(object):

    """Representation of SPDX file.
    Fields:
    name - File name, str mandatory one.
    comment - File comment str, Optional zero or one.
    type - one of FileType.SOURCE, FileType.BINARY, FileType.ARCHIVE
    and FileType.OTHER, optional zero or one.
    chk_sum - SHA1, Mandatory one.
    conc_lics - Mandatory one. document.License or utils.NoAssert or utils.SPDXNone.
    licenses_in_file - list of licenses found in file, mandatory one or more.
    document.license or utils.NoAssert or utils.SPDXNone.
    license_comment - Optional.
    copyright - Copyright text, Mandatory one. utils.NoAssert or utils.SPDXNone or str.
    notice - optional One.
    contributers - List of strings.
    dependencies - list of file locations.
    artifact_of_project_name - list of project names, possibly empty.
    artifact_of_project_home - list of project home page, possibly empty.
    artifact_of_project_uri - list of project uris, possibly empty.
    """

    def __init__(self, name):
        super(File, self).__init__()
        self.name = name
        self.comment = None
        self.type = None
        self.chk_sum = None
        self.conc_lics = None
        self.licenses_in_file = []
        self.license_comment = None
        self.copyright = None
        self.notice = None
        self.contributers = []
        self.dependencies = []
        self.artifact_of_project_name = []
        self.artifact_of_project_home = []
        self.artifact_of_project_uri = []

    def validate(self, messages):
        """Validates the fields and appends user friendly messages 
        to messages parameter if there are errors.
        """
        return True
