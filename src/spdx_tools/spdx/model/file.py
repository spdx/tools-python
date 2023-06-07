# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from dataclasses import field
from enum import Enum, auto

from beartype.typing import List, Optional, Union
from license_expression import LicenseExpression

from spdx_tools.common.typing.dataclass_with_properties import dataclass_with_properties
from spdx_tools.common.typing.type_checks import check_types_and_set_values
from spdx_tools.spdx.model import Checksum, SpdxNoAssertion, SpdxNone


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

    def __init__(
        self,
        name: str,
        spdx_id: str,
        checksums: List[Checksum],
        file_types: List[FileType] = None,
        license_concluded: Optional[Union[LicenseExpression, SpdxNoAssertion, SpdxNone]] = None,
        license_info_in_file: List[Union[LicenseExpression, SpdxNoAssertion, SpdxNone]] = None,
        license_comment: Optional[str] = None,
        copyright_text: Optional[Union[str, SpdxNoAssertion, SpdxNone]] = None,
        comment: str = None,
        notice: Optional[str] = None,
        contributors: List[str] = None,
        attribution_texts: List[str] = None,
    ):
        file_types = [] if file_types is None else file_types
        license_info_in_file = [] if license_info_in_file is None else license_info_in_file
        contributors = [] if contributors is None else contributors
        attribution_texts = [] if attribution_texts is None else attribution_texts
        check_types_and_set_values(self, locals())
