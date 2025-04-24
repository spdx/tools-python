# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from dataclasses import field
from datetime import datetime
from enum import Enum, auto

from beartype.typing import List, Optional

from spdx_tools.common.typing.dataclass_with_properties import dataclass_with_properties
from spdx_tools.common.typing.type_checks import check_types_and_set_values

from .creation_info import CreationInfo
from .element import Element
from .external_identifier import ExternalIdentifier
from .external_ref import ExternalRef
from .integrity_method import IntegrityMethod


class RelationshipType(Enum):
    AFFECTS = auto()
    AMENDED_BY = auto()
    ANCESTOR_OF = auto()
    AVAILABLE_FROM = auto()
    CONFIGURES = auto()
    CONTAINS = auto()
    COORDINATED_BY = auto()
    COPIED_TO = auto()
    DATA_FILE = auto()
    DELEGATED_TO = auto()
    DEPENDS_ON = auto()
    DESCENDANT_OF = auto()
    DESCRIBES = auto()
    DOES_NOT_AFFECT = auto()
    EXPANDS_TO = auto()
    EXPLOIT_CREATED_BY = auto()
    FIXED_BY = auto()
    FIXED_IN = auto()
    FOUND_BY = auto()
    GENERATES =  auto()
    HAS_ADDED_FILE = auto()
    HAS_ASSESSMENT_FOR = auto()
    HAS_ASSOCIATED_VULNERABILITY = auto()
    HAS_CONCLUDED_LICENSE = auto()
    HAS_DATA_FILE = auto()
    HAS_DECLARED_LICENSE = auto()
    HAS_DELETED_FILE = auto()
    HAS_DEPENDENCY_MANIFEST = auto()
    HAS_DISTRIBUTION_ARTIFACT = auto()
    HAS_DOCUMENTATION = auto()
    HAS_DYNAMIC_LINK = auto()
    HAS_EVIDENCE = auto()
    HAS_EXAMPLE = auto()
    HAS_HOST = auto()
    HAS_INPUT = auto()
    HAS_METADATA = auto()
    HAS_OPTIONAL_COMPONENT = auto()
    HAS_OPTIONAL_DEPENDENCY = auto()
    HAS_OUTPUT = auto()
    HAS_PREREQUISITE = auto()
    HAS_PROVIDED_DEPENDENCY = auto()
    HAS_REQUIREMENT = auto()
    HAS_SPECIFICATION = auto()
    HAS_STATIC_LINK = auto()
    HAS_TEST = auto()
    HAS_TEST_CASE = auto()
    HAS_VARIANT = auto()
    INVOKED_BY = auto()
    MODIFIED_BY = auto()
    OTHER = auto()
    PACKAGED_BY = auto()
    PATCHED_BY = auto()
    PUBLISHED_BY = auto()
    REPORTED_BY = auto()
    REPUBLISHED_BY = auto()
    SERIALIZED_IN_ARTIFACT = auto()
    TESTED_ON = auto()
    TRAINED_ON = auto()
    UNDER_INVESTIGATION_FOR = auto()
    USES_TOOL = auto()


class RelationshipCompleteness(Enum):
    COMPLETE = auto()
    INCOMPLETE = auto()
    NO_ASSERTION = auto()


@dataclass_with_properties
class Relationship(Element):
    # due to the inheritance we need to make all fields non-default in the __annotation__,
    # the __init__ method still raises an error if required fields are not set
    from_element: str = ""
    to: List[str] = field(default_factory=list)
    relationship_type: RelationshipType = None
    completeness: Optional[RelationshipCompleteness] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

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
    ):
        to = [] if not to else to
        verified_using = [] if not verified_using else verified_using
        external_ref = [] if not external_ref else external_ref
        external_identifier = [] if not external_identifier else external_identifier
        check_types_and_set_values(self, locals())
