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
from dataclasses import field
from enum import Enum, auto
from typing import Optional, List, Union

from spdx.model.checksum import Checksum
from common.typing.dataclass_with_properties import dataclass_with_properties
from license_expression import LicenseExpression
from spdx.model.spdx_no_assertion import SpdxNoAssertion
from spdx.model.spdx_none import SpdxNone
from common.typing.type_checks import check_types_and_set_values


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


@dataclass_with_properties
class File:
    name: str
    spdx_id: str
    checksums: List[Checksum]
    file_types: List[FileType] = field(default_factory=list)
    license_concluded: Optional[Union[LicenseExpression, SpdxNoAssertion, SpdxNone]] = None
    license_info_in_file: List[Union[LicenseExpression, SpdxNoAssertion, SpdxNone]] = field(default_factory=list)
    license_comment: Optional[str] = None
    copyright_text: Optional[Union[str, SpdxNoAssertion, SpdxNone]] = None
    comment: Optional[str] = None
    notice: Optional[str] = None
    contributors: List[str] = field(default_factory=list)
    attribution_texts: List[str] = field(default_factory=list)

    # Deprecated properties that should be replaced during parsing:
    # - file dependencies: replace by a DEPENDENCY_OF relationship (or one of the more precise versions)
    # - artifact of (3 properties): replace by an external package reference and a GENERATED_FROM relationship
    #   between the file and this package

    def __init__(self, name: str, spdx_id: str, checksums: List[Checksum], file_types: List[FileType] = None,
                 license_concluded: Optional[Union[LicenseExpression, SpdxNoAssertion, SpdxNone]] = None,
                 license_info_in_file: List[Union[LicenseExpression, SpdxNoAssertion, SpdxNone]] = None,
                 license_comment: Optional[str] = None,
                 copyright_text: Optional[Union[str, SpdxNoAssertion, SpdxNone]] = None,
                 comment: str = None, notice: Optional[str] = None,
                 contributors: List[str] = None, attribution_texts: List[str] = None):
        file_types = [] if file_types is None else file_types
        license_info_in_file = [] if license_info_in_file is None else license_info_in_file
        contributors = [] if contributors is None else contributors
        attribution_texts = [] if attribution_texts is None else attribution_texts
        check_types_and_set_values(self, locals())
