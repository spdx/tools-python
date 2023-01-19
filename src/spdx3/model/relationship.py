# Copyright (c) 2023 spdx contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#   http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from enum import Enum, auto
from typing import List, Optional

from common.typing.type_checks import check_types_and_set_values

from spdx3.model.creation_information import CreationInformation

from spdx3.model.element import Element

from common.typing.dataclass_with_properties import dataclass_with_properties
from spdx3.model.integrity_method import IntegrityMethod


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
    KNOWN = auto()
    UNKNOWN = auto()


@dataclass_with_properties
class Relationship(Element):
    # due to the inheritance we need to make all fields non-default in the __annotation__, the __init__ method still raises an error if required fields are not set
    from_element: Element = None
    to: List[Element] = None
    relationship_type: RelationshipType = None
    completeness: Optional[RelationshipCompleteness] = None

    def __init__(self, spdx_id: str, creation_info: CreationInformation, from_element: Element, to: List[Element],
                 relationship_type: RelationshipType, name: Optional[str] = None, summary: Optional[str] = None,
                 description: Optional[str] = None, comment: Optional[str] = None,
                 verified_using: Optional[List[IntegrityMethod]] = None, external_references: None = None,
                 external_identifier: None = None, extension: None = None,
                 completeness: Optional[RelationshipCompleteness] = None):
        check_types_and_set_values(self, locals())
