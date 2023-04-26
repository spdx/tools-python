# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from typing import Dict, List, Optional, Tuple, Union

from spdx_tools.spdx3.bump_from_spdx2.message import print_missing_conversion
from spdx_tools.spdx3.model import (
    CreationInformation,
    LifecycleScopeType,
    Relationship,
    RelationshipCompleteness,
    RelationshipType,
)
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
        bool,
        RelationshipType,
        Union[bool, LifecycleScopeType, None],
        Optional[SoftwareDependencyLinkType],
        Optional[DependencyConditionalityType],
    ],
] = {
    Spdx2_RelationshipType.AMENDS: (True, RelationshipType.AMENDS),
    Spdx2_RelationshipType.ANCESTOR_OF: (True, RelationshipType.ANCESTOR),
    Spdx2_RelationshipType.BUILD_DEPENDENCY_OF: (
        False,
        RelationshipType.DEPENDS_ON,
        LifecycleScopeType.BUILD,
        SoftwareDependencyLinkType.TOOL,
        None,
    ),
    Spdx2_RelationshipType.BUILD_TOOL_OF: (
        False,
        RelationshipType.DEPENDS_ON,
        LifecycleScopeType.BUILD,
        SoftwareDependencyLinkType.TOOL,
        None,
    ),
    Spdx2_RelationshipType.CONTAINED_BY: (True, RelationshipType.CONTAINS, True),
    Spdx2_RelationshipType.CONTAINS: (
        True,
        RelationshipType.CONTAINS,
    ),  # might be deleted in favor of depends on
    Spdx2_RelationshipType.COPY_OF: (True, RelationshipType.COPY),
    Spdx2_RelationshipType.DATA_FILE_OF: None,  # not defined, probably input/ output
    Spdx2_RelationshipType.DEPENDENCY_MANIFEST_OF: (
        False,
        RelationshipType.DEPENDS_ON,
        None,
        None,
        None,
    ),  # "expect purpose has been set to manifest"
    Spdx2_RelationshipType.DEPENDENCY_OF: (False, RelationshipType.DEPENDS_ON, True),
    Spdx2_RelationshipType.DEPENDS_ON: (
        False,
        RelationshipType.DEPENDS_ON,
    ),
    Spdx2_RelationshipType.DESCENDANT_OF: (True, RelationshipType.ANCESTOR, True),
    Spdx2_RelationshipType.DESCRIBED_BY: (True, RelationshipType.DESCRIBES, True),
    Spdx2_RelationshipType.DESCRIBES: (True, RelationshipType.DESCRIBES),  # might be deleted in favor of root
    # property
    Spdx2_RelationshipType.DEV_DEPENDENCY_OF: (
        False,
        RelationshipType.DEPENDS_ON,
        LifecycleScopeType.DEVELOPMENT,
        None,
        None,
    ),
    Spdx2_RelationshipType.DEV_TOOL_OF: (
        False,
        RelationshipType.DEPENDS_ON,
        LifecycleScopeType.DEVELOPMENT,
        SoftwareDependencyLinkType.TOOL,
        None,
    ),
    Spdx2_RelationshipType.DISTRIBUTION_ARTIFACT: None,  # not defined yet, purpose?
    Spdx2_RelationshipType.DOCUMENTATION_OF: (True, RelationshipType.DOCUMENTATION),
    Spdx2_RelationshipType.DYNAMIC_LINK: (
        False,
        RelationshipType.DEPENDS_ON,
        None,
        SoftwareDependencyLinkType.DYNAMIC,
        None,
    ),
    Spdx2_RelationshipType.EXAMPLE_OF: (True, RelationshipType.EXAMPLE),
    Spdx2_RelationshipType.EXPANDED_FROM_ARCHIVE: (True, RelationshipType.EXPANDED_FROM_ARCHIVE),
    Spdx2_RelationshipType.FILE_ADDED: (True, RelationshipType.FILE_ADDED),
    Spdx2_RelationshipType.FILE_DELETED: (True, RelationshipType.FILE_DELETED),
    Spdx2_RelationshipType.FILE_MODIFIED: (True, RelationshipType.FILE_MODIFIED),
    Spdx2_RelationshipType.GENERATED_FROM: (True, RelationshipType.GENERATES, True),
    Spdx2_RelationshipType.GENERATES: (True, RelationshipType.GENERATES),
    Spdx2_RelationshipType.HAS_PREREQUISITE: (
        False,
        RelationshipType.DEPENDS_ON,
        None,
        None,
        DependencyConditionalityType.PREREQUISITE,
    ),
    Spdx2_RelationshipType.METAFILE_OF: (True, RelationshipType.METAFILE),
    Spdx2_RelationshipType.OPTIONAL_COMPONENT_OF: None,  # converted to depends on and purpose? not clear
    Spdx2_RelationshipType.OPTIONAL_DEPENDENCY_OF: (
        False,
        RelationshipType.DEPENDS_ON,
        None,
        None,
        DependencyConditionalityType.OPTIONAL,
    ),
    Spdx2_RelationshipType.OTHER: (True, RelationshipType.OTHER),
    Spdx2_RelationshipType.PACKAGE_OF: (False, RelationshipType.DEPENDS_ON),
    Spdx2_RelationshipType.PATCH_APPLIED: (True, RelationshipType.PATCH, True),
    Spdx2_RelationshipType.PATCH_FOR: (True, RelationshipType.PATCH),
    Spdx2_RelationshipType.PREREQUISITE_FOR: (
        False,
        RelationshipType.DEPENDS_ON,
        None,
        None,
        DependencyConditionalityType.PREREQUISITE,
    ),
    Spdx2_RelationshipType.PROVIDED_DEPENDENCY_OF: (
        False,
        RelationshipType.DEPENDS_ON,
        LifecycleScopeType.BUILD,
        None,
        DependencyConditionalityType.PROVIDED,
    ),
    Spdx2_RelationshipType.RUNTIME_DEPENDENCY_OF: (
        False,
        RelationshipType.DEPENDS_ON,
        LifecycleScopeType.RUNTIME,
        None,
        None,
    ),
    Spdx2_RelationshipType.STATIC_LINK: (
        False,
        RelationshipType.DEPENDS_ON,
        None,
        SoftwareDependencyLinkType.STATIC,
        None,
    ),
    Spdx2_RelationshipType.TEST_CASE_OF: (True, RelationshipType.TEST_CASE),
    Spdx2_RelationshipType.TEST_DEPENDENCY_OF: (
        False,
        RelationshipType.DEPENDS_ON,
        LifecycleScopeType.TEST,
        None,
        None,
    ),
    Spdx2_RelationshipType.TEST_OF: (True, RelationshipType.TEST),
    Spdx2_RelationshipType.TEST_TOOL_OF: (
        False,
        RelationshipType.DEPENDS_ON,
        LifecycleScopeType.TEST,
        SoftwareDependencyLinkType.TOOL,
        None,
    ),
    Spdx2_RelationshipType.VARIANT_OF: (True, RelationshipType.VARIANT),
    Spdx2_RelationshipType.REQUIREMENT_DESCRIPTION_FOR: (True, RelationshipType.REQUIREMENT_FOR),
    Spdx2_RelationshipType.SPECIFICATION_FOR: (True, RelationshipType.SPECIFICATION_FOR),
}


def bump_relationships(
    spdx2_relationships: List[Spdx2_Relationship],
    payload: Payload,
    creation_information: CreationInformation,
    document_namespace: str,
):
    generated_relationships: Dict[Tuple[str, str], List[Relationship]] = {}
    for counter, spdx2_relationship in enumerate(spdx2_relationships):
        relationship = bump_relationship(spdx2_relationship, creation_information, document_namespace, counter)
        if relationship:
            generated_relationships.setdefault(
                (relationship.from_element, relationship.relationship_type.name), []
            ).append(relationship)

    for key, relationships in generated_relationships.items():
        if len(relationships) > 1:
            merge_relationships_and_add_to_payload(payload, relationships)
        else:
            payload.add_element(relationships[0])


def bump_relationship(
    spdx2_relationship: Spdx2_Relationship,
    creation_information: CreationInformation,
    document_namespace: str,
    counter: int,
) -> Optional[Union[Relationship, SoftwareDependencyRelationship]]:
    swap_direction = False
    completeness, to = determine_completeness(spdx2_relationship.related_spdx_element_id)
    spdx_id = "#".join([document_namespace, f"SPDXRef-Relationship-{counter}"])
    parameters_for_bump = relationship_mapping[spdx2_relationship.relationship_type]
    if parameters_for_bump is None:
        print_missing_conversion(spdx2_relationship.relationship_type.name, 0)
        return
    base_relationship = parameters_for_bump[0]
    relationship_type = parameters_for_bump[1]
    if not base_relationship:
        scope = parameters_for_bump[2]
        software_linkage = parameters_for_bump[3]
        conditionality = parameters_for_bump[4]
        from_element = spdx2_relationship.spdx_element_id

        return SoftwareDependencyRelationship(
            spdx_id,
            creation_information,
            from_element,
            to,
            relationship_type,
            comment=spdx2_relationship.comment,
            completeness=completeness,
            scope=scope,
            software_linkage=software_linkage,
            conditionality=conditionality,
        )

    if base_relationship and (len(parameters_for_bump) == 3):
        swap_direction = parameters_for_bump[2]
    if swap_direction:
        if not to:
            print_missing_conversion("Swapped Relationship to NoAssertion/ None", 0)
            return
        from_element = to[0]
        to = [spdx2_relationship.spdx_element_id]
    else:
        from_element = spdx2_relationship.spdx_element_id

    return Relationship(
        spdx_id,
        creation_information,
        from_element,
        to,
        relationship_type,
        comment=spdx2_relationship.comment,
        completeness=completeness,
    )


def determine_completeness(
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


def merge_relationships_and_add_to_payload(payload: Payload, relationships: List[Relationship]):
    merged_relationship = relationships[0]
    for relationship in relationships[1:]:
        merged_relationship.to += relationship.to
        if merged_relationship.comment and relationship.comment:
            merged_relationship.comment += ", " + relationship.comment
        if not merged_relationship.comment and relationship.comment:
            merged_relationship.comment = relationship.comment

    payload.add_element(merged_relationship)
