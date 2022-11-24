# Copyright (c) 2022 spdx contributors
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
from typing import Optional, List, Union

from src.model.checksum import Checksum
from src.model.license import License
from src.model.license_expression import LicenseExpression
from src.model.spdx_no_assertion import SpdxNoAssertion
from src.model.spdx_none import SpdxNone


class FileType(Enum):
    SOURCE = auto()
    BINARY = auto()
    ARCHIVE = auto()
    APPLICATION = auto()
    AUDIO = auto()
    IMAGE = auto()
    TEXT = auto()
    VIDEO = auto()
    DOCUMENTATION = auto()
    SPDX = auto()
    OTHER = auto()


class File:
    name: str
    spdx_id: str
    file_type: List[FileType]
    checksums: List[Checksum]
    concluded_license: Optional[License, SpdxNoAssertion, SpdxNone]
    license_info_in_file: Optional[List[LicenseExpression], SpdxNoAssertion, SpdxNone]
    license_comment: Optional[str]
    copyright_text: Optional[str, SpdxNoAssertion, SpdxNone]
    comment: Optional[str]
    notice: Optional[str]
    contributors: List[str]
    attribution_texts: List[str]

    # Deprecated properties that should be replaced during parsing:
    # - file dependencies: replace by a DEPENDENCY_OF relationship (or one of the more precise versions)
    # - artifact of (3 properties): replace by an external package reference and a GENERATED_FROM relationship
    #   between the file and this package

    def __init__(self, name: str, spdx_id: str, checksums: List[Checksum], file_type: List[FileType] = None,
                 comment: str = None, concluded_license: Optional[Union[License, SpdxNoAssertion, SpdxNone]] = None,
                 license_info_in_file: List[Union[LicenseExpression, SpdxNoAssertion, SpdxNone]] = None,
                 license_comment: Optional[str] = None,
                 copyright_text: Optional[Union[str, SpdxNoAssertion, SpdxNone]] = None, notice: Optional[str] = None,
                 contributors: List[str] = None, attribution_texts: List[str] = None):
        self.name = name
        self.spdx_id = spdx_id
        self.file_type = file_type or []
        self.checksums = checksums
        self.concluded_license = concluded_license or []
        self.license_info_in_file = license_info_in_file or []
        self.license_comment = license_comment
        self.copyright_text = copyright_text
        self.comment = comment
        self.notice = notice
        self.contributors = contributors or []
        self.attribution_texts = attribution_texts or []
