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
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional, List, Union

from typeguard import typechecked

from src.model.checksum import Checksum
from src.model.license import License
from src.model.license_expression import LicenseExpression
from src.model.spdx_no_assertion import SpdxNoAssertion
from src.model.spdx_none import SpdxNone
from src.model.dataclass_with_properties import dataclass_with_properties


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


@typechecked
@dataclass_with_properties
@dataclass(eq=True)
class File:
    name: str
    spdx_id: str
    file_type: List[FileType] = field(default_factory=list)
    checksums: List[Checksum] = field(default_factory=list)
    concluded_license: Optional[Union[License, SpdxNoAssertion, SpdxNone]] = None
    license_info_in_file: Optional[Union[List[LicenseExpression], SpdxNoAssertion, SpdxNone]] = field(default_factory=list)
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
