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

from functools import total_ordering
import hashlib

from spdx import checksum
from spdx import document
from spdx import utils


class FileType(object):
    SOURCE = 1
    BINARY = 2
    ARCHIVE = 3
    OTHER = 4
    APPLICATION = 5
    AUDIO = 6
    IMAGE = 7
    TEXT = 8
    DOCUMENTATION = 9
    SPDX = 10
    VIDEO = 11


FILE_TYPE_TO_XML_DICT = {
    FileType.SOURCE: "fileType_source",
    FileType.OTHER: "fileType_other",
    FileType.BINARY: "fileType_binary",
    FileType.ARCHIVE: "fileType_archive",
    FileType.APPLICATION: "fileType_application",
    FileType.AUDIO: "fileType_audio",
    FileType.DOCUMENTATION: "fileType_documentation",
    FileType.IMAGE: "fileType_image",
    FileType.SPDX: "fileType_spdx",
    FileType.TEXT: "fileType_text",
    FileType.VIDEO: "fileType_video"
}
FILE_TYPE_TO_STRING_DICT = {
    FileType.SOURCE: "SOURCE",
    FileType.OTHER: "OTHER",
    FileType.BINARY: "BINARY",
    FileType.ARCHIVE: "ARCHIVE",
    FileType.APPLICATION: "APPLICATION",
    FileType.AUDIO: "AUDIO",
    FileType.DOCUMENTATION: "DOCUMENTATION",
    FileType.IMAGE: "IMAGE",
    FileType.SPDX: "SPDX",
    FileType.TEXT: "TEXT",
    FileType.VIDEO: "VIDEO",
}

FILE_TYPE_FROM_XML_DICT = {
    "fileType_source": FileType.SOURCE,
    "fileType_binary": FileType.BINARY,
    "fileType_archive": FileType.ARCHIVE,
    "fileType_other": FileType.OTHER,
    "fileType_application": FileType.APPLICATION,
    "fileType_audio": FileType.AUDIO,
    "fileType_image": FileType.IMAGE,
    "fileType_text": FileType.TEXT,
    "fileType_documentation": FileType.DOCUMENTATION,
    "fileType_spdx": FileType.SPDX,
    "fileType_video": FileType.VIDEO,
}

FILE_TYPE_FROM_STRING_DICT = {
    "SOURCE": FileType.SOURCE,
    "BINARY": FileType.BINARY,
    "ARCHIVE": FileType.ARCHIVE,
    "OTHER": FileType.OTHER,
    "APPLICATION": FileType.APPLICATION,
    "AUDIO": FileType.AUDIO,
    "IMAGE": FileType.IMAGE,
    "TEXT": FileType.TEXT,
    "DOCUMENTATION": FileType.DOCUMENTATION,
    "SPDX": FileType.SPDX,
    "VIDEO": FileType.VIDEO,
}


@total_ordering
class File(object):
    """
    Represent an SPDX file.
    Fields:
    - name: File name, str mandatory one.
    - spdx_id: Uniquely identify any element in an SPDX document which may be
    referenced by other elements. Mandatory, one. Type: str.
    - comment: File comment str, Optional zero or one.
      file_types: list of file types.  cardinality 1..#FILE_TYPES
    - chk_sums: list of checksums, there must be a SHA1 hash, at least.
    - conc_lics: Mandatory one. document.License or utils.NoAssert or utils.SPDXNone.
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

    def __init__(self, name, spdx_id=None):
        self.name = name
        self.spdx_id = spdx_id
        self.comment = None
        self.file_types = []
        self.checksums = []
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
    def chk_sum(self):
        """
        Backwards compatibility, return first checksum.
        """
        return self.get_checksum('SHA1')

    @chk_sum.setter
    def chk_sum(self, value):
        self.set_checksum(value)

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
        if not isinstance(
            self.copyright,
            (str, utils.NoAssert, utils.SPDXNone),
        ):
            messages.append(
                "File copyright must be str or unicode or "
                "utils.NoAssert or utils.SPDXNone"
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
        # FIXME: what are we testing the length of a list? or?
        if len(self.licenses_in_file) == 0:
            messages.append("File must have at least one license in file.")

        return messages

    def validate_concluded_license(self, messages):
        # FIXME: use isinstance instead??
        if not isinstance(
            self.conc_lics, (document.License, utils.NoAssert, utils.SPDXNone)
        ):
            messages.append(
                "File concluded license must be one of "
                "document.License, utils.NoAssert or utils.SPDXNone"
            )

        return messages

    def validate_file_types(self, messages):
        if len(self.file_types) < 1:
            messages.append('At least one file type must be specified.')
        return messages

    def validate_checksum(self, messages):
        if self.get_checksum() is None:
            messages.append("At least one file checksum algorithm must be SHA1")
        return messages

    def calculate_checksum(self, hash_algorithm='SHA1'):
        BUFFER_SIZE = 65536

        file_hash = hashlib.new(hash_algorithm.lower())
        with open(self.name, "rb") as file_handle:
            while True:
                data = file_handle.read(BUFFER_SIZE)
                if not data:
                    break
                file_hash.update(data)

        return file_hash.hexdigest()

    def get_checksum(self, hash_algorithm='SHA1'):
        for chk_sum in self.checksums:
            if chk_sum.identifier == hash_algorithm:
                return chk_sum
        return None

    def set_checksum(self, chk_sum):
        if isinstance(chk_sum, checksum.Algorithm):
            for file_chk_sum in self.checksums:
                if file_chk_sum.identifier == chk_sum.identifier:
                    file_chk_sum.value = chk_sum.value
                    return
            self.checksums.append(chk_sum)

    def has_optional_field(self, field):
        return getattr(self, field, None) is not None
