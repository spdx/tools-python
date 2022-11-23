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

from enum import Enum, auto
from functools import total_ordering
import hashlib

from spdx import checksum
from spdx import utils
from spdx.license import License
from spdx.parsers.builderexceptions import SPDXValueError


class FileType(Enum):
    SOURCE = auto()
    BINARY = auto()
    ARCHIVE = auto()
    OTHER = auto()
    APPLICATION = auto()
    AUDIO = auto()
    IMAGE = auto()
    TEXT = auto()
    DOCUMENTATION = auto()
    SPDX = auto()
    VIDEO = auto()


def file_type_from_rdf(rdf_file_type: str) -> FileType:
    """e.g. convert fileType_source to FileType.SOURCE"""
    file_type_str = rdf_file_type.split("_")[1].upper()

    if file_type_str not in FileType.__members__:
        raise SPDXValueError("File:FileType")

    return FileType[file_type_str]


def file_type_to_rdf(file_type: FileType) -> str:
    """e.g. convert SOURCE to fileType_source"""
    return f"fileType_{file_type.name.lower()}"


@total_ordering
class File(object):
    """
    Represent an SPDX file.
    Fields:
    - name: File name, str mandatory one.
    - spdx_id: Uniquely identify any element in an SPDX document which may be
    referenced by other elements. Mandatory, one. Type: str.
    - comment: File comment str, Optional zero or one.
    - file_types: list of file types. Cardinality 0..*
    - chksum: SHA1, Mandatory one.
    - conc_lics: Mandatory one. license.License or utils.NoAssert or utils.SPDXNone.
    - licenses_in_file: list of licenses found in file, mandatory one or more.
      document.License or utils.SPDXNone or utils.NoAssert.
    - document.license or utils.NoAssert or utils.SPDXNone.
    - license_comment: Optional.
    - copyright: Copyright text, Mandatory one. utils.NoAssert or utils.SPDXNone or str.
    - notice: optional One, str.
    - contributors: List of strings.
    - dependencies: list of file locations.
    - artifact_of_project_name: list of project names, possibly empty.
    - artifact_of_project_home: list of project home page, possibly empty.
    - artifact_of_project_uri: list of project uris, possibly empty.
    -attribution_text: optional string.
    """

    def __init__(self, name, spdx_id=None, chksum=None):
        self.name = name
        self.spdx_id = spdx_id
        self.comment = None
        self.file_types = []
        self.checksums = [chksum]
        self.conc_lics = None
        self.licenses_in_file = []
        self.license_comment = None
        self.copyright = None
        self.notice = None
        self.attribution_text = None
        self.contributors = []
        self.dependencies = []
        self.artifact_of_project_name = []
        self.artifact_of_project_home = []
        self.artifact_of_project_uri = []

    def __eq__(self, other):
        return isinstance(other, File) and self.name == other.name

    def __lt__(self, other):
        return self.name < other.name

    @property
    def chksum(self):
        """
        Backwards compatibility, return first checksum.
        """
        # NOTE Package.check_sum but File.chk_sum
        return self.checksums[0]

    @chksum.setter
    def chksum(self, value):
        self.checksums[0] = value

    def add_lics(self, lics):
        self.licenses_in_file.append(lics)

    def add_contrib(self, contrib):
        self.contributors.append(contrib)

    def add_depend(self, depend):
        self.dependencies.append(depend)

    def add_artifact(self, symbol, value):
        """
        Add value as artifact_of_project{symbol}.
        """
        symbol = "artifact_of_project_{}".format(symbol)
        artifact = getattr(self, symbol)
        artifact.append(value)

    def validate(self, messages):
        """
        Check that all the fields are valid.
        Appends any error messages to messages parameter shall be a ErrorMessages.
        """
        messages.push_context(self.name)
        self.validate_concluded_license(messages)
        self.validate_file_types(messages)
        self.validate_checksum(messages)
        self.validate_licenses_in_file(messages)
        self.validate_copyright(messages)
        self.validate_artifacts(messages)
        self.validate_spdx_id(messages)
        messages.pop_context()
        return messages

    def validate_spdx_id(self, messages):
        if self.spdx_id is None:
            messages.append("File has no SPDX Identifier.")

        return messages

    def validate_copyright(self, messages):
        if self.copyright and not isinstance(
            self.copyright,
            (str, utils.NoAssert, utils.SPDXNone),
        ):
            messages.append(
                "File copyright must be str or unicode or "
                "spdx.utils.NoAssert or spdx.utils.SPDXNone"
            )

        return messages

    def validate_artifacts(self, messages):
        if len(self.artifact_of_project_home) < max(
            len(self.artifact_of_project_uri), len(self.artifact_of_project_name)
        ):
            messages.append(
                "File must have as much artifact of project as uri or homepage"
            )

        return messages

    def validate_licenses_in_file(self, messages):
        for license_in_file in self.licenses_in_file:
            if not isinstance(
                license_in_file, (utils.SPDXNone, utils.NoAssert, License)
            ):
                messages.append(
                    "License in file must be instance of "
                    "spdx.utils.SPDXNone or spdx.utils.NoAssert or "
                    "spdx.license.License"
                )

        return messages

    def validate_concluded_license(self, messages):
        if self.conc_lics and not isinstance(
            self.conc_lics, (utils.SPDXNone, utils.NoAssert, License)
        ):
            messages.append(
                "File concluded license must be instance of "
                "spdx.utils.SPDXNone or spdx.utils.NoAssert or "
                "spdx.license.License"
            )

        return messages

    def validate_file_types(self, messages):
        for file_type in self.file_types:
            if not isinstance(file_type, FileType):
                messages.append(f"{file_type} is not of type FileType.")
        return messages

    def validate_checksum(self, messages):
        if not isinstance(self.chksum, checksum.Algorithm):
            messages.append(
                "File checksum must be instance of spdx.checksum.Algorithm"
            )
        else:
            if not self.chksum.identifier == "SHA1":
                messages.append("File checksum algorithm must be SHA1")

        return messages

    def calc_chksum(self):
        BUFFER_SIZE = 65536

        file_sha1 = hashlib.sha1()
        with open(self.name, "rb") as file_handle:
            while True:
                data = file_handle.read(BUFFER_SIZE)
                if not data:
                    break
                file_sha1.update(data)

        return file_sha1.hexdigest()

    def has_optional_field(self, field):
        return bool (getattr(self, field, None))
