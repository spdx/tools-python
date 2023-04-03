# SPDX-FileCopyrightText: 2023 spdx contributors

# SPDX-License-Identifier: Apache-2.0
from dataclasses import field
from enum import Enum, auto
from typing import List, Optional

from common.typing.dataclass_with_properties import dataclass_with_properties
from common.typing.type_checks import check_types_and_set_values


class ExternalReferenceType(Enum):
    ALT_DOWNLOAD_LOCATION = auto()
    ALT_WEB_PAGE = auto()
    OTHER = auto()
    SECURITY_ADVISORY = auto()
    SECURITY_FIX = auto()
    SECURITY_OTHER = auto()


@dataclass_with_properties
class ExternalReference:
    external_reference_type: Optional[ExternalReferenceType] = None
    locator: List[str] = field(default_factory=list)
    content_type: Optional[str] = None  # placeholder for MediaType
    comment: Optional[str] = None

    def __init__(
        self,
        external_reference_type: Optional[ExternalReferenceType] = None,
        locator: List[str] = None,
        content_type: Optional[str] = None,
        comment: Optional[str] = None,
    ):
        locator = [] if locator is None else locator
        check_types_and_set_values(self, locals())
