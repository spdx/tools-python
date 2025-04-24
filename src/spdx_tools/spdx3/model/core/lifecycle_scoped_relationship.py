# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from datetime import datetime
from enum import Enum, auto

from beartype.typing import List, Optional

from spdx_tools.common.typing.dataclass_with_properties import dataclass_with_properties
from spdx_tools.common.typing.type_checks import check_types_and_set_values

from .creation_info import CreationInfo
from .external_identifier import ExternalIdentifier
from .external_ref import ExternalRef
from .integrity_method import IntegrityMethod
from .relationship import Relationship, RelationshipCompleteness, RelationshipType


class LifecycleScopeType(Enum):
    BUILD = auto()
    DESIGN = auto()
    DEVELOPMENT = auto()
    OTHER = auto()
    RUNTIME = auto()
    TEST = auto()


@dataclass_with_properties
class LifecycleScopedRelationship(Relationship):
    scope: Optional[LifecycleScopeType] = None

    def __init__(
        self,
        spdx_id: str,
        from_element: str,
        relationship_type: RelationshipType,
        to: List[str] = [],
        creation_info: Optional[CreationInfo] = None,
        name: Optional[str] = None,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        comment: Optional[str] = None,
        verified_using: List[IntegrityMethod] = [],
        external_ref: List[ExternalRef] = [],
        external_identifier: List[ExternalIdentifier] = [],
        extension: Optional[str] = None,
        completeness: Optional[RelationshipCompleteness] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        scope: Optional[LifecycleScopeType] = None,
    ):
        to = [] if not to else to
        verified_using = [] if not verified_using else verified_using
        external_ref = [] if not external_ref else external_ref
        external_identifier = [] if not external_identifier else external_identifier
        check_types_and_set_values(self, locals())
