# Copyright (c) 2023 spdx contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#    http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from typing import Tuple, Optional

from spdx.model.relationship import Relationship as Spdx2_Relationship
from spdx.model.relationship import RelationshipType as Spdx2_RelationshipType
from spdx.model.spdx_no_assertion import SpdxNoAssertion
from spdx.model.spdx_none import SpdxNone
from spdx3.model.creation_information import CreationInformation
from spdx3.model.relationship import Relationship, RelationshipType, RelationshipCompleteness


def bump_relationship(spdx2_relationship: Spdx2_Relationship,
                      creation_information: CreationInformation, counter: int) -> Relationship:
    relationship_type, swap_direction = bump_relationship_type(spdx2_relationship.relationship_type)

    if isinstance(spdx2_relationship.related_spdx_element_id,
                  SpdxNoAssertion):  # how to translate none/ no assertion to element?
        completeness = RelationshipCompleteness.UNKNOWN
    elif isinstance(spdx2_relationship.related_spdx_element_id, SpdxNone):
        completeness = RelationshipCompleteness.KNOWN
    else:
        completeness = None

    if swap_direction:
        from_element = spdx2_relationship.related_spdx_element_id
        to = [spdx2_relationship.spdx_element_id]
    else:
        from_element = spdx2_relationship.spdx_element_id
        to = [spdx2_relationship.related_spdx_element_id]
    comment = spdx2_relationship.comment

    relationship = Relationship(f"SPDXRef-Relationship-{counter}", creation_information, from_element, to,
                                relationship_type, comment=comment, completeness=completeness)

    return relationship


def bump_relationship_type(spdx2_relationship_type: Spdx2_RelationshipType) -> Optional[Tuple[RelationshipType, bool]]:
    if spdx2_relationship_type == Spdx2_RelationshipType.DESCRIBED_BY:
        return RelationshipType.DESCRIBES, True
    if spdx2_relationship_type == Spdx2_RelationshipType.CONTAINED_BY:
        return RelationshipType.CONTAINS, True
    if spdx2_relationship_type == Spdx2_RelationshipType.DEPENDENCY_OF:
        return RelationshipType.DEPENDS_ON, True
    if spdx2_relationship_type == Spdx2_RelationshipType.GENERATED_FROM:
        return RelationshipType.GENERATES, True
    if spdx2_relationship_type == Spdx2_RelationshipType.HAS_PREREQUISITE:
        return RelationshipType.PREREQUISITE, True
    if spdx2_relationship_type.name.endswith("_OF"):
        relationship_type = spdx2_relationship_type.name.replace("_OF", "")
        return RelationshipType[relationship_type], False
    if spdx2_relationship_type.name.endswith("_FOR"):
        relationship_type = spdx2_relationship_type.name.replace("_FOR", "")
        return RelationshipType[relationship_type], False
    return RelationshipType[spdx2_relationship_type.name], False
    # if spdx2_relationship_type == Spdx2_RelationshipType.PATCH_APPLIED:
    #     print_missing_conversion("RelationshipType.PATCH_APPLIED", 0)
    #     return None
