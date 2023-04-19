# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from enum import Enum, auto
from typing import List, Optional

from spdx_tools.common.typing.dataclass_with_properties import dataclass_with_properties
from spdx_tools.common.typing.type_checks import check_types_and_set_values
from spdx_tools.spdx3.model import (
    CreationInformation,
    ExternalIdentifier,
    ExternalReference,
    IntegrityMethod,
    Relationship,
    RelationshipCompleteness,
    RelationshipType,
)


class LifecycleScopeType(Enum):
    DESIGN = auto()
    BUILD = auto()
    DEVELOPMENT = auto()
    TEST = auto()
    RUNTIME = auto()
    OTHER = auto()


@dataclass_with_properties
class LifecycleScopedRelationship(Relationship):
    scope: Optional[LifecycleScopeType] = None

    def __init__(
        self,
        spdx_id: str,
        creation_info: CreationInformation,
        from_element: str,
        to: List[str],
        relationship_type: RelationshipType,
        name: Optional[str] = None,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        comment: Optional[str] = None,
        verified_using: List[IntegrityMethod] = None,
        external_references: List[ExternalReference] = None,
        external_identifier: List[ExternalIdentifier] = None,
        extension: None = None,
        completeness: Optional[RelationshipCompleteness] = None,
        scope: Optional[LifecycleScopeType] = None,
    ):
        verified_using = [] if verified_using is None else verified_using
        external_references = [] if external_references is None else external_references
        external_identifier = [] if external_identifier is None else external_identifier
        check_types_and_set_values(self, locals())
