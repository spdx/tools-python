# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from enum import Enum, auto
from typing import Optional

from common.typing.dataclass_with_properties import dataclass_with_properties
from common.typing.type_checks import check_types_and_set_values


class ExternalIdentifierType(Enum):
    CPE22 = auto()
    CPE23 = auto()
    EMAIL = auto()
    GITOID = auto()
    PURL = auto()
    SWHID = auto()
    SWID = auto()
    URL_SCHEME = auto()
    OTHER = auto()


@dataclass_with_properties
class ExternalIdentifier:
    external_identifier_type: ExternalIdentifierType
    identifier: str
    comment: Optional[str] = None

    def __init__(
        self, external_identifier_type: ExternalIdentifierType, identifier: str, comment: Optional[str] = None
    ):
        check_types_and_set_values(self, locals())
