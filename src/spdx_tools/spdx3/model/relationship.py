# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from enum import Enum, auto
from typing import List, Optional

from spdx_tools.common.typing.dataclass_with_properties import dataclass_with_properties
from spdx_tools.common.typing.type_checks import check_types_and_set_values
from spdx_tools.spdx3.model import CreationInformation, Element, ExternalIdentifier, ExternalReference, IntegrityMethod


class RelationshipType(Enum):
    AMENDS = auto()
    ANCESTOR = auto()
    BUILD_DEPENDENCY = auto()
    BUILD_TOOL = auto()
    CONTAINS = auto()
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
    DYNAMIC_LINK = auto()
    EXAMPLE = auto()
    EXPANDED_FROM_ARCHIVE = auto()
    FILE_ADDED = auto()
    FILE_DELETED = auto()
    FILE_MODIFIED = auto()
    GENERATES = auto()
    METAFILE = auto()
    OPTIONAL_COMPONENT = auto()
    OPTIONAL_DEPENDENCY = auto()
    OTHER = auto()
    PACKAGES = auto()
    PATCH = auto()
    PREREQUISITE = auto()
    PROVIDED_DEPENDENCY = auto()
    REQUIREMENT_FOR = auto()
    RUNTIME_DEPENDENCY = auto()
    SPECIFICATION_FOR = auto()
    STATIC_LINK = auto()
    SUPPLIED_BY = auto()
    TEST = auto()
    TEST_CASE = auto()
    TEST_DEPENDENCY = auto()
    TEST_TOOL = auto()
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
    to: List[str] = None
    relationship_type: RelationshipType = None
    completeness: Optional[RelationshipCompleteness] = None

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
    ):
        verified_using = [] if verified_using is None else verified_using
        external_references = [] if external_references is None else external_references
        external_identifier = [] if external_identifier is None else external_identifier
        check_types_and_set_values(self, locals())
