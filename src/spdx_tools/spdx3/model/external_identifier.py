# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from dataclasses import field
from enum import Enum, auto

from beartype.typing import List, Optional

from spdx_tools.common.typing.dataclass_with_properties import dataclass_with_properties
from spdx_tools.common.typing.type_checks import check_types_and_set_values


class ExternalIdentifierType(Enum):
    CPE22 = auto()
    CPE23 = auto()
    CVE = auto()
    EMAIL = auto()
    GITOID = auto()
    PURL = auto()
    SECURITY_OTHER = auto()
    SWHID = auto()
    SWID = auto()
    URL_SCHEME = auto()
    OTHER = auto()


@dataclass_with_properties
class ExternalIdentifier:
    external_identifier_type: ExternalIdentifierType
    identifier: str
    comment: Optional[str] = None
    identifier_locator: List[str] = field(default_factory=list)
    issuing_authority: Optional[str] = None

    def __init__(
        self,
        external_identifier_type: ExternalIdentifierType,
        identifier: str,
        comment: Optional[str] = None,
        identifier_locator: List[str] = None,
        issuing_authority: Optional[str] = None,
    ):
        identifier_locator = [] if identifier_locator is None else identifier_locator
        check_types_and_set_values(self, locals())
