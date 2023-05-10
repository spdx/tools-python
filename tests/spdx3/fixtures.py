# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from datetime import datetime

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
    NamespaceMap,
    Organization,
    Person,
    Relationship,
    RelationshipCompleteness,
    RelationshipType,
    SoftwareAgent,
    SpdxDocument,
    Tool,
)

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
    profile = ["core"] if profile is None else profile  # TODO: this should use the Enum
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


def agent_fixture(
    spdx_id="https://spdx.test/tools-python/agent_fixture",
    creation_info=creation_info_fixture(),
    name="agentName",
    summary="agentSummary",
    description="agentDescription",
    comment="agentComment",
    verified_using=None,
    external_references=None,
    external_identifier=None,
    extension=None,
) -> Agent:
    verified_using = [hash_fixture()] if verified_using is None else verified_using
    external_references = [external_reference_fixture()] if external_references is None else external_references
    external_identifier = [external_identifier_fixture()] if external_identifier is None else external_identifier
    return Agent(
        spdx_id=spdx_id,
        creation_info=creation_info,
        name=name,
        summary=summary,
        description=description,
        comment=comment,
        verified_using=verified_using,
        external_references=external_references,
        external_identifier=external_identifier,
        extension=extension,
    )


def annotation_fixture(
    spdx_id="https://spdx.test/tools-python/annotation_fixture",
    creation_info=creation_info_fixture(),
    annotation_type=AnnotationType.OTHER,
    subject="https://spdx.test/tools-python/annotation_subject",
    name="annotationName",
    summary="annotationSummary",
    description="annotationDescription",
    comment="annotationComment",
    verified_using=None,
    external_references=None,
    external_identifier=None,
    extension=None,
    content_type="annotationContentType",
    statement="annotationStatement",
) -> Annotation:
    verified_using = [hash_fixture()] if verified_using is None else verified_using
    external_references = [external_reference_fixture()] if external_references is None else external_references
    external_identifier = [external_identifier_fixture()] if external_identifier is None else external_identifier
    return Annotation(
        spdx_id=spdx_id,
        creation_info=creation_info,
        annotation_type=annotation_type,
        subject=subject,
        name=name,
        summary=summary,
        description=description,
        comment=comment,
        verified_using=verified_using,
        external_references=external_references,
        external_identifier=external_identifier,
        extension=extension,
        content_type=content_type,
        statement=statement,
    )


def bom_fixture(
    spdx_id="https://spdx.test/tools-python/bom_fixture",
    creation_info=creation_info_fixture(),
    elements=None,
    root_elements=None,
    name="bomName",
    summary="bomSummary",
    description="bomDescription",
    comment="bomComment",
    verified_using=None,
    external_references=None,
    external_identifier=None,
    extension=None,
    namespaces=None,
    imports=None,
    context="bomContext",
) -> Bom:
    elements = ["https://spdx.test/tools-python/bom_element"] if elements is None else elements
    root_elements = ["https://spdx.test/tools-python/bom_root_element"] if root_elements is None else root_elements
    verified_using = [hash_fixture()] if verified_using is None else verified_using
    external_references = [external_reference_fixture()] if external_references is None else external_references
    external_identifier = [external_identifier_fixture()] if external_identifier is None else external_identifier
    namespaces = [namespace_map_fixture()] if namespaces is None else namespaces
    imports = [external_map_fixture()] if imports is None else imports
    return Bom(
        spdx_id=spdx_id,
        creation_info=creation_info,
        element=elements,
        root_element=root_elements,
        name=name,
        summary=summary,
        description=description,
        comment=comment,
        verified_using=verified_using,
        external_references=external_references,
        external_identifier=external_identifier,
        extension=extension,
        namespaces=namespaces,
        imports=imports,
        context=context,
    )


def bundle_fixture(
    spdx_id="https://spdx.test/tools-python/bundle_fixture",
    creation_info=creation_info_fixture(),
    elements=None,
    root_elements=None,
    name="bundleName",
    summary="bundleSummary",
    description="bundleDescription",
    comment="bundleComment",
    verified_using=None,
    external_references=None,
    external_identifier=None,
    extension=None,
    namespaces=None,
    imports=None,
    context="bundleContext",
) -> Bundle:
    elements = ["https://spdx.test/tools-python/bundle_element"] if elements is None else elements
    root_elements = ["https://spdx.test/tools-python/bundle_root_element"] if root_elements is None else root_elements
    verified_using = [hash_fixture()] if verified_using is None else verified_using
    external_references = [external_reference_fixture()] if external_references is None else external_references
    external_identifier = [external_identifier_fixture()] if external_identifier is None else external_identifier
    namespaces = [namespace_map_fixture()] if namespaces is None else namespaces
    imports = [external_map_fixture()] if imports is None else imports
    return Bundle(
        spdx_id=spdx_id,
        creation_info=creation_info,
        element=elements,
        root_element=root_elements,
        name=name,
        summary=summary,
        description=description,
        comment=comment,
        verified_using=verified_using,
        external_references=external_references,
        external_identifier=external_identifier,
        extension=extension,
        namespaces=namespaces,
        imports=imports,
        context=context,
    )


def organization_fixture(
    spdx_id="https://spdx.test/tools-python/organization_fixture",
    creation_info=creation_info_fixture(),
    name="organizationName",
    summary="organizationSummary",
    description="organizationDescription",
    comment="organizationComment",
    verified_using=None,
    external_references=None,
    external_identifier=None,
    extension=None,
) -> Organization:
    verified_using = [hash_fixture()] if verified_using is None else verified_using
    external_references = [external_reference_fixture()] if external_references is None else external_references
    external_identifier = [external_identifier_fixture()] if external_identifier is None else external_identifier
    return Organization(
        spdx_id=spdx_id,
        creation_info=creation_info,
        name=name,
        summary=summary,
        description=description,
        comment=comment,
        verified_using=verified_using,
        external_references=external_references,
        external_identifier=external_identifier,
        extension=extension,
    )


def person_fixture(
    spdx_id="https://spdx.test/tools-python/person_fixture",
    creation_info=creation_info_fixture(),
    name="personName",
    summary="personSummary",
    description="personDescription",
    comment="personComment",
    verified_using=None,
    external_references=None,
    external_identifier=None,
    extension=None,
) -> Person:
    verified_using = [hash_fixture()] if verified_using is None else verified_using
    external_references = [external_reference_fixture()] if external_references is None else external_references
    external_identifier = [external_identifier_fixture()] if external_identifier is None else external_identifier
    return Person(
        spdx_id=spdx_id,
        creation_info=creation_info,
        name=name,
        summary=summary,
        description=description,
        comment=comment,
        verified_using=verified_using,
        external_references=external_references,
        external_identifier=external_identifier,
        extension=extension,
    )


def relationship_fixture(
    spdx_id="https://spdx.test/tools-python/relationship_fixture",
    creation_info=creation_info_fixture(),
    from_element="https://spdx.test/tools-python/relationship_from_element",
    to=None,
    relationship_type=RelationshipType.OTHER,
    name="relationshipName",
    summary="relationshipSummary",
    description="relationshipDescription",
    comment="relationshipComment",
    verified_using=None,
    external_references=None,
    external_identifier=None,
    extension=None,
    completeness=RelationshipCompleteness.COMPLETE,
) -> Relationship:
    to = ["https://spdx.test/tools-python/relationship_to"] if to is None else to
    verified_using = [hash_fixture()] if verified_using is None else verified_using
    external_references = [external_reference_fixture()] if external_references is None else external_references
    external_identifier = [external_identifier_fixture()] if external_identifier is None else external_identifier
    return Relationship(
        spdx_id=spdx_id,
        creation_info=creation_info,
        from_element=from_element,
        to=to,
        relationship_type=relationship_type,
        name=name,
        summary=summary,
        description=description,
        comment=comment,
        verified_using=verified_using,
        external_references=external_references,
        external_identifier=external_identifier,
        extension=extension,
        completeness=completeness,
    )


def software_agent_fixture(
    spdx_id="https://spdx.test/tools-python/software_agent_fixture",
    creation_info=creation_info_fixture(),
    name="softwareAgentName",
    summary="softwareAgentSummary",
    description="softwareAgentDescription",
    comment="softwareAgentComment",
    verified_using=None,
    external_references=None,
    external_identifier=None,
    extension=None,
) -> SoftwareAgent:
    verified_using = [hash_fixture()] if verified_using is None else verified_using
    external_references = [external_reference_fixture()] if external_references is None else external_references
    external_identifier = [external_identifier_fixture()] if external_identifier is None else external_identifier
    return SoftwareAgent(
        spdx_id=spdx_id,
        creation_info=creation_info,
        name=name,
        summary=summary,
        description=description,
        comment=comment,
        verified_using=verified_using,
        external_references=external_references,
        external_identifier=external_identifier,
        extension=extension,
    )


def spdx_document_fixture(
    spdx_id="https://spdx.test/tools-python/spdx_document_fixture",
    creation_info=creation_info_fixture(),
    name="spdxDocumentName",
    elements=None,
    root_elements=None,
    summary="spdxDocumentSummary",
    description="spdxDocumentDescription",
    comment="spdxDocumentComment",
    verified_using=None,
    external_references=None,
    external_identifier=None,
    extension=None,
    namespaces=None,
    imports=None,
    context="context_spdx_document",
) -> SpdxDocument:
    elements = ["https://spdx.test/tools-python/spdx_document_element"] if elements is None else elements
    root_elements = (
        ["https://spdx.test/tools-python/spdx_document_root_element"] if root_elements is None else root_elements
    )
    verified_using = [hash_fixture()] if verified_using is None else verified_using
    external_references = [external_reference_fixture()] if external_references is None else external_references
    external_identifier = [external_identifier_fixture()] if external_identifier is None else external_identifier
    namespaces = [namespace_map_fixture()] if namespaces is None else namespaces
    imports = [external_map_fixture()] if imports is None else imports
    return SpdxDocument(
        spdx_id=spdx_id,
        creation_info=creation_info,
        name=name,
        element=elements,
        root_element=root_elements,
        summary=summary,
        description=description,
        comment=comment,
        verified_using=verified_using,
        external_references=external_references,
        external_identifier=external_identifier,
        extension=extension,
        namespaces=namespaces,
        imports=imports,
        context=context,
    )


def tool_fixture(
    spdx_id="https://spdx.test/tools-python/tool_fixture",
    creation_info=creation_info_fixture(),
    name="toolName",
    summary="toolSummary",
    description="toolDescription",
    comment="toolComment",
    verified_using=None,
    external_references=None,
    external_identifier=None,
    extension=None,
) -> Tool:
    verified_using = [hash_fixture()] if verified_using is None else verified_using
    external_references = [external_reference_fixture()] if external_references is None else external_references
    external_identifier = [external_identifier_fixture()] if external_identifier is None else external_identifier
    return Tool(
        spdx_id=spdx_id,
        creation_info=creation_info,
        name=name,
        summary=summary,
        description=description,
        comment=comment,
        verified_using=verified_using,
        external_references=external_references,
        external_identifier=external_identifier,
        extension=extension,
    )
