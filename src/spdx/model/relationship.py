# Copyright (c) 2022 spdx contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from enum import auto, Enum
from typing import Optional, Union

from spdx.model.spdx_no_assertion import SpdxNoAssertion
from spdx.model.spdx_none import SpdxNone
from common.typing.dataclass_with_properties import dataclass_with_properties
from common.typing.type_checks import check_types_and_set_values


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

    def __init__(self, spdx_element_id: str, relationship_type: RelationshipType,
                 related_spdx_element_id: Union[str, SpdxNone, SpdxNoAssertion], comment: Optional[str] = None):
        check_types_and_set_values(self, locals())
