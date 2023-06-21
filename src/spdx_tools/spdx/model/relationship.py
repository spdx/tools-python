# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from enum import Enum, auto

from beartype.typing import Optional, Union

from spdx_tools.common.typing.dataclass_with_properties import dataclass_with_properties
from spdx_tools.common.typing.type_checks import check_types_and_set_values
from spdx_tools.spdx.model import SpdxNoAssertion, SpdxNone


class RelationshipType(Enum):
    AMENDS = auto()
    ANCESTOR_OF = auto()
    BUILD_DEPENDENCY_OF = auto()
    BUILD_TOOL_OF = auto()
    CONTAINED_BY = auto()
    CONTAINS = auto()
    COPY_OF = auto()
    DATA_FILE_OF = auto()
    DEPENDENCY_MANIFEST_OF = auto()
    DEPENDENCY_OF = auto()
    DEPENDS_ON = auto()
    DESCENDANT_OF = auto()
    DESCRIBED_BY = auto()
    DESCRIBES = auto()
    DEV_DEPENDENCY_OF = auto()
    DEV_TOOL_OF = auto()
    DISTRIBUTION_ARTIFACT = auto()
    DOCUMENTATION_OF = auto()
    DYNAMIC_LINK = auto()
    EXAMPLE_OF = auto()
    EXPANDED_FROM_ARCHIVE = auto()
    FILE_ADDED = auto()
    FILE_DELETED = auto()
    FILE_MODIFIED = auto()
    GENERATED_FROM = auto()
    GENERATES = auto()
    HAS_PREREQUISITE = auto()
    METAFILE_OF = auto()
    OPTIONAL_COMPONENT_OF = auto()
    OPTIONAL_DEPENDENCY_OF = auto()
    OTHER = auto()
    PACKAGE_OF = auto()
    PATCH_APPLIED = auto()
    PATCH_FOR = auto()
    PREREQUISITE_FOR = auto()
    PROVIDED_DEPENDENCY_OF = auto()
    REQUIREMENT_DESCRIPTION_FOR = auto()
    RUNTIME_DEPENDENCY_OF = auto()
    SPECIFICATION_FOR = auto()
    STATIC_LINK = auto()
    TEST_CASE_OF = auto()
    TEST_DEPENDENCY_OF = auto()
    TEST_OF = auto()
    TEST_TOOL_OF = auto()
    VARIANT_OF = auto()


@dataclass_with_properties
class Relationship:
    spdx_element_id: str
    relationship_type: RelationshipType
    related_spdx_element_id: Union[str, SpdxNone, SpdxNoAssertion]
    comment: Optional[str] = None

    def __init__(
        self,
        spdx_element_id: str,
        relationship_type: RelationshipType,
        related_spdx_element_id: Union[str, SpdxNone, SpdxNoAssertion],
        comment: Optional[str] = None,
    ):
        check_types_and_set_values(self, locals())
