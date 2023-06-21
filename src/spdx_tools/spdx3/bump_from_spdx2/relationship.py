# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import logging
import sys

from beartype.typing import Dict, List, Optional, Tuple, Union

from spdx_tools.spdx3.bump_from_spdx2.message import print_missing_conversion
from spdx_tools.spdx3.model import LifecycleScopeType, Relationship, RelationshipCompleteness, RelationshipType
from spdx_tools.spdx3.model.software import (
    DependencyConditionalityType,
    SoftwareDependencyLinkType,
    SoftwareDependencyRelationship,
)
from spdx_tools.spdx3.payload import Payload
from spdx_tools.spdx.model.relationship import Relationship as Spdx2_Relationship
from spdx_tools.spdx.model.relationship import RelationshipType as Spdx2_RelationshipType
from spdx_tools.spdx.model.spdx_no_assertion import SpdxNoAssertion
from spdx_tools.spdx.model.spdx_none import SpdxNone

# bump relationship type, map each relationship type to the corresponding class in 3.0,
# the relationship type, other arguments and if swapped
relationship_mapping: Dict[
    Spdx2_RelationshipType,
    Tuple[
        Union[Relationship, SoftwareDependencyRelationship],
        RelationshipType,
        Dict[str, Union[bool, LifecycleScopeType, SoftwareDependencyLinkType, DependencyConditionalityType]],
    ],
] = {
    Spdx2_RelationshipType.AMENDS: (Relationship, RelationshipType.AMENDS, {}),
    Spdx2_RelationshipType.ANCESTOR_OF: (Relationship, RelationshipType.ANCESTOR, {}),
    Spdx2_RelationshipType.BUILD_DEPENDENCY_OF: (
        SoftwareDependencyRelationship,
        RelationshipType.DEPENDS_ON,
        {
            "scope": LifecycleScopeType.BUILD,
            "linkage": SoftwareDependencyLinkType.TOOL,
        },
    ),
    Spdx2_RelationshipType.BUILD_TOOL_OF: (
        SoftwareDependencyRelationship,
        RelationshipType.DEPENDS_ON,
        {"scope": LifecycleScopeType.BUILD, "linkage": SoftwareDependencyLinkType.TOOL},
    ),
    Spdx2_RelationshipType.CONTAINED_BY: (Relationship, RelationshipType.CONTAINS, {"swap": True}),
    Spdx2_RelationshipType.CONTAINS: (
        Relationship,
        RelationshipType.CONTAINS,
        {},
    ),  # might be deleted in favor of depends on
    Spdx2_RelationshipType.COPY_OF: (Relationship, RelationshipType.COPY, {}),
    Spdx2_RelationshipType.DATA_FILE_OF: (None, None, {}),  # not defined, probably input/ output
    Spdx2_RelationshipType.DEPENDENCY_MANIFEST_OF: (
        SoftwareDependencyRelationship,
        RelationshipType.DEPENDS_ON,
        {},
    ),  # "expect purpose has been set to manifest"
    Spdx2_RelationshipType.DEPENDENCY_OF: (
        SoftwareDependencyRelationship,
        RelationshipType.DEPENDS_ON,
        {"swap": True},
    ),
    Spdx2_RelationshipType.DEPENDS_ON: (SoftwareDependencyRelationship, RelationshipType.DEPENDS_ON, {}),
    Spdx2_RelationshipType.DESCENDANT_OF: (Relationship, RelationshipType.ANCESTOR, {"swap": True}),
    Spdx2_RelationshipType.DESCRIBED_BY: (Relationship, RelationshipType.DESCRIBES, {"swap": True}),
    Spdx2_RelationshipType.DESCRIBES: (
        Relationship,
        RelationshipType.DESCRIBES,
        {},
    ),  # might be deleted in favor of root
    # property
    Spdx2_RelationshipType.DEV_DEPENDENCY_OF: (
        SoftwareDependencyRelationship,
        RelationshipType.DEPENDS_ON,
        {"scope": LifecycleScopeType.DEVELOPMENT},
    ),
    Spdx2_RelationshipType.DEV_TOOL_OF: (
        SoftwareDependencyRelationship,
        RelationshipType.DEPENDS_ON,
        {"scope": LifecycleScopeType.DEVELOPMENT, "linkage": SoftwareDependencyLinkType.TOOL},
    ),
    Spdx2_RelationshipType.DISTRIBUTION_ARTIFACT: (None, None, {}),  # not defined yet, purpose?
    Spdx2_RelationshipType.DOCUMENTATION_OF: (Relationship, RelationshipType.DOCUMENTATION, {}),
    Spdx2_RelationshipType.DYNAMIC_LINK: (
        SoftwareDependencyRelationship,
        RelationshipType.DEPENDS_ON,
        {"linkage": SoftwareDependencyLinkType.DYNAMIC},
    ),
    Spdx2_RelationshipType.EXAMPLE_OF: (Relationship, RelationshipType.EXAMPLE, {}),
    Spdx2_RelationshipType.EXPANDED_FROM_ARCHIVE: (Relationship, RelationshipType.EXPANDED_FROM_ARCHIVE, {}),
    Spdx2_RelationshipType.FILE_ADDED: (Relationship, RelationshipType.FILE_ADDED, {}),
    Spdx2_RelationshipType.FILE_DELETED: (Relationship, RelationshipType.FILE_DELETED, {}),
    Spdx2_RelationshipType.FILE_MODIFIED: (Relationship, RelationshipType.FILE_MODIFIED, {}),
    Spdx2_RelationshipType.GENERATED_FROM: (Relationship, RelationshipType.GENERATES, {"swap": True}),
    Spdx2_RelationshipType.GENERATES: (Relationship, RelationshipType.GENERATES, {}),
    Spdx2_RelationshipType.HAS_PREREQUISITE: (
        SoftwareDependencyRelationship,
        RelationshipType.DEPENDS_ON,
        {"conditionality": DependencyConditionalityType.PREREQUISITE},
    ),
    Spdx2_RelationshipType.METAFILE_OF: (Relationship, RelationshipType.METAFILE, {}),
    Spdx2_RelationshipType.OPTIONAL_COMPONENT_OF: (None, None, {}),  # converted to depends on and purpose? not clear
    Spdx2_RelationshipType.OPTIONAL_DEPENDENCY_OF: (
        SoftwareDependencyRelationship,
        RelationshipType.DEPENDS_ON,
        {"conditionality": DependencyConditionalityType.OPTIONAL},
    ),
    Spdx2_RelationshipType.OTHER: (Relationship, RelationshipType.OTHER, {}),
    Spdx2_RelationshipType.PACKAGE_OF: (SoftwareDependencyRelationship, RelationshipType.DEPENDS_ON, {}),
    Spdx2_RelationshipType.PATCH_APPLIED: (Relationship, RelationshipType.PATCH, {"swap": True}),
    Spdx2_RelationshipType.PATCH_FOR: (Relationship, RelationshipType.PATCH, {}),
    Spdx2_RelationshipType.PREREQUISITE_FOR: (
        SoftwareDependencyRelationship,
        RelationshipType.DEPENDS_ON,
        {"conditionality": DependencyConditionalityType.PREREQUISITE},
    ),
    Spdx2_RelationshipType.PROVIDED_DEPENDENCY_OF: (
        SoftwareDependencyRelationship,
        RelationshipType.DEPENDS_ON,
        {"scope": LifecycleScopeType.BUILD, "conditionality": DependencyConditionalityType.PROVIDED},
    ),
    Spdx2_RelationshipType.RUNTIME_DEPENDENCY_OF: (
        SoftwareDependencyRelationship,
        RelationshipType.DEPENDS_ON,
        {"scope": LifecycleScopeType.RUNTIME},
    ),
    Spdx2_RelationshipType.STATIC_LINK: (
        SoftwareDependencyRelationship,
        RelationshipType.DEPENDS_ON,
        {"linkage": SoftwareDependencyLinkType.STATIC},
    ),
    Spdx2_RelationshipType.TEST_CASE_OF: (Relationship, RelationshipType.TEST_CASE, {}),
    Spdx2_RelationshipType.TEST_DEPENDENCY_OF: (
        SoftwareDependencyRelationship,
        RelationshipType.DEPENDS_ON,
        {"scope": LifecycleScopeType.TEST},
    ),
    Spdx2_RelationshipType.TEST_OF: (Relationship, RelationshipType.TEST, {}),
    Spdx2_RelationshipType.TEST_TOOL_OF: (
        SoftwareDependencyRelationship,
        RelationshipType.DEPENDS_ON,
        {"scope": LifecycleScopeType.TEST, "linkage": SoftwareDependencyLinkType.TOOL},
    ),
    Spdx2_RelationshipType.VARIANT_OF: (Relationship, RelationshipType.VARIANT, {}),
    Spdx2_RelationshipType.REQUIREMENT_DESCRIPTION_FOR: (Relationship, RelationshipType.REQUIREMENT_FOR, {}),
    Spdx2_RelationshipType.SPECIFICATION_FOR: (Relationship, RelationshipType.SPECIFICATION_FOR, {}),
}


def bump_relationships(
    spdx2_relationships: List[Spdx2_Relationship],
    payload: Payload,
    document_namespace: str,
):
    generated_relationships: Dict[Tuple[str, str], List[Relationship]] = {}
    for counter, spdx2_relationship in enumerate(spdx2_relationships):
        relationship = bump_relationship(spdx2_relationship, document_namespace, counter)
        if relationship:
            generated_relationships.setdefault(
                (relationship.from_element, relationship.relationship_type.name), []
            ).append(relationship)

    for relationships in generated_relationships.values():
        if len(relationships) > 1:
            _merge_relationships_and_add_to_payload(relationships, payload)
        else:
            payload.add_element(relationships[0])


def bump_relationship(
    spdx2_relationship: Spdx2_Relationship,
    document_namespace: str,
    counter: int,
) -> Optional[Union[Relationship, SoftwareDependencyRelationship]]:
    completeness, to = determine_completeness_and_to(spdx2_relationship.related_spdx_element_id)
    spdx_id = "#".join([document_namespace, f"SPDXRef-Relationship-{counter}"])
    relationship_class, relationship_type, parameters = relationship_mapping[spdx2_relationship.relationship_type]
    if relationship_class is None:
        print_missing_conversion(spdx2_relationship.relationship_type.name, 0)
        return

    swap_direction = parameters.get("swap", False)

    if swap_direction:
        if not to:
            print_missing_conversion("Swapped Relationship to NoAssertion/None", 0)
            return
        from_element = to[0]
        to = [spdx2_relationship.spdx_element_id]
    else:
        from_element = spdx2_relationship.spdx_element_id

    if relationship_class == SoftwareDependencyRelationship:
        from_element = spdx2_relationship.spdx_element_id

        return SoftwareDependencyRelationship(
            spdx_id,
            f"{document_namespace}#{from_element}",
            relationship_type,
            [f"{document_namespace}#{t}" for t in to],
            comment=spdx2_relationship.comment,
            completeness=completeness,
            scope=parameters.get("scope"),
            software_linkage=parameters.get("linkage"),
            conditionality=parameters.get("conditionality"),
        )

    return Relationship(
        spdx_id,
        f"{document_namespace}#{from_element}",
        relationship_type,
        [f"{document_namespace}#{t}" for t in to],
        comment=spdx2_relationship.comment,
        completeness=completeness,
    )


def determine_completeness_and_to(
    related_spdx_element_id: Union[str, SpdxNone, SpdxNoAssertion]
) -> Tuple[Optional[RelationshipCompleteness], List[str]]:
    if isinstance(related_spdx_element_id, SpdxNoAssertion):
        completeness = RelationshipCompleteness.NOASSERTION
        to = []
    elif isinstance(related_spdx_element_id, SpdxNone):
        completeness = RelationshipCompleteness.COMPLETE
        to = []
    else:
        completeness = None
        to = [related_spdx_element_id]
    return completeness, to


def _merge_relationships_and_add_to_payload(relationships: List[Relationship], payload: Payload):
    to = []
    completeness = None
    spdx_id = None
    merged_relationship = relationships[0]
    for merged_relationship in relationships:
        if merged_relationship.comment:
            payload.add_element(merged_relationship)
            continue
        if merged_relationship.completeness:
            if completeness and completeness != merged_relationship.completeness:
                logging.warning(
                    f"Contradicting information about completeness of relationship: {merged_relationship}", sys.stderr
                )
            else:
                completeness = merged_relationship.completeness

        to += merged_relationship.to
        spdx_id = merged_relationship.spdx_id
    if to:
        merged_relationship.spdx_id = spdx_id
        merged_relationship.to = to
        merged_relationship.completeness = completeness
        merged_relationship.comment = None
        payload.add_element(merged_relationship)
