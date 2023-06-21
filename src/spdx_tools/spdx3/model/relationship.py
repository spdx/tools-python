# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from dataclasses import field
from datetime import datetime
from enum import Enum, auto

from beartype.typing import List, Optional

from spdx_tools.common.typing.dataclass_with_properties import dataclass_with_properties
from spdx_tools.common.typing.type_checks import check_types_and_set_values
from spdx_tools.spdx3.model import CreationInfo, Element, ExternalIdentifier, ExternalReference, IntegrityMethod


class RelationshipType(Enum):
    AFFECTS = auto()
    AMENDS = auto()
    ANCESTOR = auto()
    AVAILABLE_FROM = auto()
    BUILD_DEPENDENCY = auto()
    BUILD_TOOL = auto()
    COORDINATED_BY = auto()
    CONTAINS = auto()
    CONFIG_OF = auto()
    COPY = auto()
    DATA_FILE = auto()
    DEPENDENCY_MANIFEST = auto()
    DEPENDS_ON = auto()
    DESCENDANT = auto()
    DESCRIBES = auto()
    DEV_DEPENDENCY = auto()
    DEV_TOOL = auto()
    DISTRIBUTION_ARTIFACT = auto()
    DOCUMENTATION = auto()
    DOES_NOT_AFFECT = auto()
    DYNAMIC_LINK = auto()
    EXAMPLE = auto()
    EVIDENCE_FOR = auto()
    EXPANDED_FROM_ARCHIVE = auto()
    EXPLOIT_CREATED_BY = auto()
    FILE_ADDED = auto()
    FILE_DELETED = auto()
    FILE_MODIFIED = auto()
    FIXED_BY = auto()
    FIXED_IN = auto()
    FOUND_BY = auto()
    GENERATES = auto()
    HAS_ASSESSMENT_FOR = auto()
    HAS_ASSOCIATED_VULNERABILITY = auto()
    HOST_OF = auto()
    INPUT_OF = auto()
    INVOKED_BY = auto()
    METAFILE = auto()
    ON_BEHALF_OF = auto()
    OPTIONAL_COMPONENT = auto()
    OPTIONAL_DEPENDENCY = auto()
    OTHER = auto()
    OUTPUT_OF = auto()
    PACKAGES = auto()
    PATCH = auto()
    PREREQUISITE = auto()
    PROVIDED_DEPENDENCY = auto()
    PUBLISHED_BY = auto()
    REPORTED_BY = auto()
    REPUBLISHED_BY = auto()
    REQUIREMENT_FOR = auto()
    RUNTIME_DEPENDENCY = auto()
    SPECIFICATION_FOR = auto()
    STATIC_LINK = auto()
    TEST = auto()
    TEST_CASE = auto()
    TEST_DEPENDENCY = auto()
    TEST_TOOL = auto()
    TESTED_ON = auto()
    TRAINED_ON = auto()
    UNDER_INVESTIGATION_FOR = auto()
    VARIANT = auto()


class RelationshipCompleteness(Enum):
    INCOMPLETE = auto()
    COMPLETE = auto()
    NOASSERTION = auto()


@dataclass_with_properties
class Relationship(Element):
    # due to the inheritance we need to make all fields non-default in the __annotation__,
    # the __init__ method still raises an error if required fields are not set
    from_element: str = None
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
    ):
        to = [] if to is None else to
        verified_using = [] if verified_using is None else verified_using
        external_reference = [] if external_reference is None else external_reference
        external_identifier = [] if external_identifier is None else external_identifier
        check_types_and_set_values(self, locals())
