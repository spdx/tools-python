# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from spdx_tools.spdx3.model import (
    Agent,
    Annotation,
    AnnotationType,
    Bom,
    Bundle,
    CreationInfo,
    ExternalIdentifier,
    ExternalIdentifierType,
    ExternalMap,
    ExternalReference,
    ExternalReferenceType,
    Hash,
    HashAlgorithm,
    LifecycleScopedRelationship,
    LifecycleScopeType,
    NamespaceMap,
    Organization,
    Person,
    ProfileIdentifier,
    Relationship,
    RelationshipCompleteness,
    RelationshipType,
    SoftwareAgent,
    SpdxDocument,
    Tool,
)
from spdx_tools.spdx3.model.ai import AIPackage
from spdx_tools.spdx3.model.build import Build
from spdx_tools.spdx3.model.dataset import Dataset
from spdx_tools.spdx3.model.positive_integer_range import PositiveIntegerRange
from spdx_tools.spdx3.model.software import (
    DependencyConditionalityType,
    File,
    Package,
    Sbom,
    SBOMType,
    Snippet,
    SoftwareDependencyLinkType,
    SoftwareDependencyRelationship,
    SoftwarePurpose,
)

CLASS_DICT = {
    "Agent": Agent,
    "AIPackage": AIPackage,
    "Annotation": Annotation,
    "Bom": Bom,
    "Build": Build,
    "Bundle": Bundle,
    "CreationInfo": CreationInfo,
    "Dataset": Dataset,
    "ExternalIdentifier": ExternalIdentifier,
    "ExternalMap": ExternalMap,
    "ExternalReference": ExternalReference,
    "File": File,
    "Hash": Hash,
    "LifecycleScopedRelationship": LifecycleScopedRelationship,
    "NamespaceMap": NamespaceMap,
    "Organization": Organization,
    "Package": Package,
    "Person": Person,
    "PositiveIntegerRange": PositiveIntegerRange,
    "Relationship": Relationship,
    "Sbom": Sbom,
    "Snippet": Snippet,
    "SoftwareAgent": SoftwareAgent,
    "SoftwareDependencyRelationship": SoftwareDependencyRelationship,
    "SpdxDocument": SpdxDocument,
    "Tool": Tool,
}
ENUM_DICT = {
    "algorithm": HashAlgorithm,
    "annotationType": AnnotationType,
    "completeness": RelationshipCompleteness,
    "conditionality": DependencyConditionalityType,
    "externalIdentifierType": ExternalIdentifierType,
    "externalReferenceType": ExternalReferenceType,
    "profile": ProfileIdentifier,
    "primaryPurpose": SoftwarePurpose,
    "additionalPurpose": SoftwarePurpose,
    "relationshipType": RelationshipType,
    "sbomType": SBOMType,
    "scope": LifecycleScopeType,
    "softwareLinkage": SoftwareDependencyLinkType,
}
SPECIALLY_TREATED_KEYS = {"from": "from_element"}
KEYS_WITH_URI_VALUES = [
    "createdBy",
    "createdUsing",
    "dataLicense",
    "from",
    "originatedBy",
    "subject",
    "suppliedBy",
    "to",
]
DATETIME_PROPERTIES = ["created", "builtTime", "releaseTime", "validUntilTime"]
VERSION_PROPERTIES = ["specVersion"]
