# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from datetime import datetime
from typing import Any, Dict, Type

from semantic_version import Version

from spdx_tools.spdx3.model import (
    Agent,
    Annotation,
    AnnotationType,
    Bom,
    Bundle,
    CreationInformation,
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
from spdx_tools.spdx3.model.software import Sbom, SBOMType

"""Utility methods to create data model instances. All properties have valid defaults, so they don't need to be
specified unless relevant for the test."""


def creation_info_fixture(
    spec_version=Version("3.0.0"),
    created=datetime(2022, 12, 1),
    created_by=None,
    created_using=None,
    profile=None,
    data_license="CC0-1.0",
    comment="creationInfoComment",
) -> CreationInformation:
    created_by = ["https://spdx.test/tools-python/creation_info_created_by"] if created_by is None else created_by
    created_using = (
        ["https://spdx.test/tools-python/creation_info_created_using"] if created_using is None else created_using
    )
    profile = (
        [ProfileIdentifier.CORE, ProfileIdentifier.SOFTWARE, ProfileIdentifier.LICENSING]
        if profile is None
        else profile
    )
    return CreationInformation(
        spec_version=spec_version,
        created=created,
        created_by=created_by,
        created_using=created_using,
        profile=profile,
        data_license=data_license,
        comment=comment,
    )


def external_identifier_fixture(
    external_identifier_type=ExternalIdentifierType.OTHER,
    identifier="externalIdentifierIdentifier",
    comment="externalIdentifierComment",
    identifier_locator=None,
    issuing_authority="https://spdx.test/tools-python/external_identifier_issuing_authority",
) -> ExternalIdentifier:
    identifier_locator = (
        ["https://spdx.test/tools-python/external_identifier_identifier_locator"]
        if identifier_locator is None
        else identifier_locator
    )
    return ExternalIdentifier(
        external_identifier_type=external_identifier_type,
        identifier=identifier,
        comment=comment,
        identifier_locator=identifier_locator,
        issuing_authority=issuing_authority,
    )


def external_reference_fixture(
    external_reference_type=ExternalReferenceType.OTHER,
    locator=None,
    content_type="externalReferenceContentType",
    comment="externalReferenceComment",
) -> ExternalReference:
    locator = ["org.apache.tomcat:tomcat:9.0.0.M4"] if locator is None else locator
    return ExternalReference(
        external_reference_type=external_reference_type, locator=locator, content_type=content_type, comment=comment
    )


def hash_fixture(
    algorithm=HashAlgorithm.SHA1,
    hash_value="71c4025dd9897b364f3ebbb42c484ff43d00791c",
    comment="hashComment",
) -> Hash:
    return Hash(algorithm=algorithm, hash_value=hash_value, comment=comment)


def external_map_fixture(
    external_id="https://spdx.test/tools-python/external_map_external_id",
    verified_using=None,
    location_hint="https://spdx.test/tools-python/external_map_location_hint",
) -> ExternalMap:
    verified_using = [hash_fixture()] if verified_using is None else verified_using
    return ExternalMap(external_id=external_id, verified_using=verified_using, location_hint=location_hint)


def namespace_map_fixture(
    prefix="namespaceMapPrefix", namespace="https://spdx.test/tools-python/namespace_map_namespace"
) -> NamespaceMap:
    return NamespaceMap(prefix=prefix, namespace=namespace)


ELEMENT_DICT = {
    "spdx_id": "https://spdx.test/tools-python/element_fixture",
    "creation_info": creation_info_fixture(),
    "name": "elementName",
    "summary": "elementSummary",
    "description": "elementDescription",
    "comment": "elementComment",
    "verified_using": [hash_fixture()],
    "external_references": [external_reference_fixture()],
    "external_identifier": [external_identifier_fixture()],
    "extension": "extensionPlaceholder",
}

RELATIONSHIP_DICT = {
    "from_element": "https://spdx.test/tools-python/relationship_from_element",
    "relationship_type": RelationshipType.OTHER,
    "to": ["https://spdx.test/tools-python/relationship_to"],
    "completeness": RelationshipCompleteness.COMPLETE,
    "start_time": datetime(2020, 1, 1),
    "end_time": datetime(2023, 1, 1),
}

LIFECYCLE_SCOPED_RELATIONSHIP_DICT = {"scope": LifecycleScopeType.DESIGN}

ANNOTATION_DICT = {
    "annotation_type": AnnotationType.OTHER,
    "subject": "https://spdx.test/tools-python/annotation_subject",
    "content_type": ["annotationContent"],
    "statement": "annotationStatement",
}

ELEMENT_COLLECTION_DICT = {
    "element": ["https://spdx.test/tools-python/collection_element"],
    "root_element": ["https://spdx.test/tools-python/collection_root_element"],
    "namespaces": [namespace_map_fixture()],
    "imports": [external_map_fixture()],
}

BUNDLE_DICT = {
    "context": "bundleContext",
}

SBOM_DICT = {
    "sbom_type": [SBOMType.BUILD],
}

FIXTURE_DICTS = {
    Agent: [ELEMENT_DICT],
    Person: [ELEMENT_DICT],
    Organization: [ELEMENT_DICT],
    SoftwareAgent: [ELEMENT_DICT],
    Tool: [ELEMENT_DICT],
    Relationship: [ELEMENT_DICT, RELATIONSHIP_DICT],
    LifecycleScopedRelationship: [ELEMENT_DICT, RELATIONSHIP_DICT, LIFECYCLE_SCOPED_RELATIONSHIP_DICT],
    Annotation: [ELEMENT_DICT, ANNOTATION_DICT],
    Bundle: [ELEMENT_DICT, ELEMENT_COLLECTION_DICT, BUNDLE_DICT],
    SpdxDocument: [ELEMENT_DICT, ELEMENT_COLLECTION_DICT, BUNDLE_DICT],
    Bom: [ELEMENT_DICT, ELEMENT_COLLECTION_DICT, BUNDLE_DICT],
    Sbom: [ELEMENT_DICT, ELEMENT_COLLECTION_DICT, BUNDLE_DICT, SBOM_DICT],
}


def element_fixture_factory(clazz: Type[Any], **kwargs) -> Any:
    fixture_dict = get_fixture_dict(clazz)

    for key in kwargs.keys():
        if key not in fixture_dict.keys():
            raise ValueError(f"Provided property name {key} is not part of {clazz.__name__}.")
        else:
            fixture_dict[key] = kwargs[key]

    return clazz(**fixture_dict)


def get_fixture_dict(clazz: Type[Any]) -> Dict[str, Any]:
    fixture_dict = {}
    if clazz not in FIXTURE_DICTS.keys():
        raise ValueError(
            f"{clazz.__name__} is not part of the FIXTURE_DICTS. "
            f"If it is a non-abstract subclass of Element, it was probably forgotten to add."
        )
    for property_dict in FIXTURE_DICTS[clazz]:
        fixture_dict.update(property_dict)

    fixture_dict["spdx_id"] = f"https://spdx.test/tools-python/{clazz.__name__}_fixture"

    return fixture_dict
