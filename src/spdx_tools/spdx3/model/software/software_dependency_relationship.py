# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from datetime import datetime
from enum import Enum, auto

from beartype.typing import List, Optional

from spdx_tools.common.typing.dataclass_with_properties import dataclass_with_properties
from spdx_tools.common.typing.type_checks import check_types_and_set_values
from spdx_tools.spdx3.model import (
    CreationInfo,
    ExternalIdentifier,
    ExternalReference,
    IntegrityMethod,
    LifecycleScopedRelationship,
    LifecycleScopeType,
    RelationshipCompleteness,
    RelationshipType,
)


class SoftwareDependencyLinkType(Enum):
    STATIC = auto()
    DYNAMIC = auto()
    TOOL = auto()
    OTHER = auto()


class DependencyConditionalityType(Enum):
    OPTIONAL = auto()
    REQUIRED = auto()
    PROVIDED = auto()
    PREREQUISITE = auto()
    OTHER = auto()


@dataclass_with_properties
class SoftwareDependencyRelationship(LifecycleScopedRelationship):
    software_linkage: Optional[SoftwareDependencyLinkType] = None
    conditionality: Optional[DependencyConditionalityType] = None

    def __init__(
        self,
        spdx_id: str,
        from_element: str,
        relationship_type: RelationshipType,
        to: List[str] = None,
        creation_info: Optional[CreationInfo] = None,
        name: Optional[str] = None,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        comment: Optional[str] = None,
        verified_using: List[IntegrityMethod] = None,
        external_reference: List[ExternalReference] = None,
        external_identifier: List[ExternalIdentifier] = None,
        extension: Optional[str] = None,
        completeness: Optional[RelationshipCompleteness] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        scope: Optional[LifecycleScopeType] = None,
        software_linkage: Optional[SoftwareDependencyLinkType] = None,
        conditionality: Optional[DependencyConditionalityType] = None,
    ):
        to = [] if to is None else to
        verified_using = [] if verified_using is None else verified_using
        external_reference = [] if external_reference is None else external_reference
        external_identifier = [] if external_identifier is None else external_identifier
        check_types_and_set_values(self, locals())
