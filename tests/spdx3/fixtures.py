# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from datetime import datetime

from semantic_version import Version

from spdx_tools.spdx3.model.agent import Agent
from spdx_tools.spdx3.model.annotation import Annotation, AnnotationType
from spdx_tools.spdx3.model.bom import Bom
from spdx_tools.spdx3.model.bundle import Bundle
from spdx_tools.spdx3.model.creation_information import CreationInformation
from spdx_tools.spdx3.model.external_identifier import ExternalIdentifier, ExternalIdentifierType
from spdx_tools.spdx3.model.external_map import ExternalMap
from spdx_tools.spdx3.model.external_reference import ExternalReference, ExternalReferenceType
from spdx_tools.spdx3.model.hash import Hash, HashAlgorithm
from spdx_tools.spdx3.model.namespace_map import NamespaceMap
from spdx_tools.spdx3.model.organization import Organization
from spdx_tools.spdx3.model.person import Person
from spdx_tools.spdx3.model.relationship import Relationship, RelationshipCompleteness, RelationshipType
from spdx_tools.spdx3.model.software_agent import SoftwareAgent
from spdx_tools.spdx3.model.spdx_document import SpdxDocument
from spdx_tools.spdx3.model.tool import Tool

"""Utility methods to create data model instances. All properties have valid defaults, so they don't need to be
specified unless relevant for the test."""


def creation_info_fixture(
    spec_version=Version("3.0.0"),
    created=datetime(2022, 12, 1),
    created_by=["creatorCreationInfo"],
    created_using=["createdCreationInfo"],
    profile=["profileCreationInfo"],
    data_license="CC0-1.0",
    comment="commentCreationInfo",
) -> CreationInformation:
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
    external_identifier_type=ExternalIdentifierType.OTHER, identifier="identifier_ext_iden", comment="comment_ext_iden"
) -> ExternalIdentifier:
    return ExternalIdentifier(external_identifier_type, identifier, comment)


def external_reference_fixture(
    external_reference_type=ExternalReferenceType.OTHER,
    locator=None,
    content_type="content_type_exter_ref",
    comment="comment_exter_ref",
) -> ExternalReference:
    locator = ["locator for external reference"] if locator is None else locator
    return ExternalReference(external_reference_type, locator, content_type, comment)


def hash_fixture(algorithm=HashAlgorithm.SHA1, hash_value="hash_value", comment="comment_hash_algorithm") -> Hash:
    return Hash(algorithm=algorithm, hash_value=hash_value, comment=comment)


def external_map_fixture(
    external_id="https://spdx.test/tools-python/ExternalMapFixture",
    verified_using=None,
    location_hint="https://spdx.test/tools-python/location_hint_ExternalMap",
) -> ExternalMap:
    verified_using = [hash_fixture()] if verified_using is None else verified_using
    return ExternalMap(external_id=external_id, verified_using=verified_using, location_hint=location_hint)


def namespace_map_fixture(prefix="prefix_namespace_map", namespace="namespace_namespace_map") -> NamespaceMap:
    return NamespaceMap(prefix=prefix, namespace=namespace)


def agent_fixture(
    spdx_id="https://spdx.test/tools-python/AgentFixture",
    creation_info=creation_info_fixture(),
    name="nameAgent",
    summary="summaryAgent",
    description="descriptionAgent",
    comment="commentAgent",
    verified_using=[hash_fixture()],
    external_references=[external_reference_fixture()],
    external_identifier=[external_identifier_fixture()],
    extension=None,
) -> Agent:
    verified_using = [] if verified_using is None else verified_using
    external_references = [] if external_references is None else external_references
    external_identifier = [] if external_identifier is None else external_identifier
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
    spdx_id="https://spdx.test/tools-python/AnnotationFixture",
    creation_info=creation_info_fixture(),
    annotation_type=AnnotationType.OTHER,
    subject="subject_annotation",
    name="name_annotation",
    summary="summary_annotation",
    description="description_annotation",
    comment="comment_annotation",
    verified_using=[hash_fixture()],
    external_references=[external_reference_fixture()],
    external_identifier=[external_identifier_fixture()],
    extension=None,
    content_type="content_type_annotation",
    statement="statement_annotation",
) -> Annotation:
    verified_using = [] if verified_using is None else verified_using
    external_references = [] if external_references is None else external_references
    external_identifier = [] if external_identifier is None else external_identifier
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
    spdx_id="https://spdx.test/tools-python/BomFixture",
    creation_info=creation_info_fixture(),
    elements=["elements_bom"],
    root_elements=["root_elements_bom"],
    name="name_bom",
    summary="summary_bom",
    description="description_bom",
    comment="comment_bom",
    verified_using=[hash_fixture()],
    external_references=[external_reference_fixture()],
    external_identifier=[external_identifier_fixture()],
    extension=None,
    namespaces=[namespace_map_fixture()],
    imports=[external_map_fixture()],
    context=None,
) -> Bom:
    verified_using = [] if verified_using is None else verified_using
    external_references = [] if external_references is None else external_references
    external_identifier = [] if external_identifier is None else external_identifier
    namespaces = [] if namespaces is None else namespaces
    imports = [] if imports is None else imports
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
    spdx_id="https://spdx.test/tools-python/BundleFixture",
    creation_info=creation_info_fixture(),
    elements=["elements_bundle"],
    root_elements=["root_elements_bundle"],
    name="name_bundle",
    summary="summary_bundle",
    description="description_bundle",
    comment="comment_bundle",
    verified_using=[hash_fixture()],
    external_references=[external_reference_fixture()],
    external_identifier=[external_identifier_fixture()],
    extension=None,
    namespaces=[namespace_map_fixture()],
    imports=[external_map_fixture()],
    context="context_bundle",
) -> Bundle:
    verified_using = [] if verified_using is None else verified_using
    external_references = [] if external_references is None else external_references
    external_identifier = [] if external_identifier is None else external_identifier
    namespaces = [] if namespaces is None else namespaces
    imports = [] if imports is None else imports
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
    spdx_id="https://spdx.test/tools-python/OrganizationFixture",
    creation_info=creation_info_fixture(),
    name="name_organization",
    summary="summary_organization",
    description="description_organization",
    comment="comment_organization",
    verified_using=[hash_fixture()],
    external_references=[external_reference_fixture()],
    external_identifier=[external_identifier_fixture()],
    extension=None,
) -> Organization:
    verified_using = [] if verified_using is None else verified_using
    external_references = [] if external_references is None else external_references
    external_identifier = [] if external_identifier is None else external_identifier
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
    spdx_id="https://spdx.test/tools-python/PersonFixture",
    creation_info=creation_info_fixture(),
    name="name_person",
    summary="summary_person",
    description="description_person",
    comment="comment_person",
    verified_using=[hash_fixture()],
    external_references=[external_reference_fixture()],
    external_identifier=[external_identifier_fixture()],
    extension=None,
) -> Person:
    verified_using = [] if verified_using is None else verified_using
    external_references = [] if external_references is None else external_references
    external_identifier = [] if external_identifier is None else external_identifier
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
    spdx_id="https://spdx.test/tools-python/RelationshipFixture",
    creation_info=creation_info_fixture(),
    from_element="from_element_relationship",
    to=["to_relationship"],
    relationship_type=RelationshipType.OTHER,
    name="name_relationship",
    summary="summary_relationship",
    description="description_relationship",
    comment="comment_relationship",
    verified_using=[hash_fixture()],
    external_references=[external_reference_fixture()],
    external_identifier=[external_identifier_fixture()],
    extension=None,
    completeness=RelationshipCompleteness.UNKNOWN,
) -> Relationship:
    verified_using = [] if verified_using is None else verified_using
    external_references = [] if external_references is None else external_references
    external_identifier = [] if external_identifier is None else external_identifier
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
    spdx_id="https://spdx.test/tools-python/SoftwareAgentFixture",
    creation_info=creation_info_fixture(),
    name="name_software_agent",
    summary="summary_software_agent",
    description="description_software_agent",
    comment="comment_software_agent",
    verified_using=[hash_fixture()],
    external_references=[external_reference_fixture()],
    external_identifier=[external_identifier_fixture()],
    extension=None,
) -> SoftwareAgent:
    verified_using = [] if verified_using is None else verified_using
    external_references = [] if external_references is None else external_references
    external_identifier = [] if external_identifier is None else external_identifier
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
    spdx_id="https://spdx.test/tools-python/SpdxDocumentFixture",
    creation_info=creation_info_fixture(),
    name="name_spdx_document",
    elements=["elements_spdx_document"],
    root_elements=["root_elements_spdx_document"],
    summary="summary_spdx_document",
    description="description_spdx_document",
    comment="comment_spdx_document",
    verified_using=[hash_fixture()],
    external_references=[external_reference_fixture()],
    external_identifier=[external_identifier_fixture()],
    extension=None,
    namespaces=[namespace_map_fixture()],
    imports=[external_map_fixture()],
    context="context_spdx_document",
) -> SpdxDocument:
    verified_using = [] if verified_using is None else verified_using
    external_references = [] if external_references is None else external_references
    external_identifier = [] if external_identifier is None else external_identifier
    namespaces = [] if namespaces is None else namespaces
    imports = [] if imports is None else imports
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
    spdx_id="https://spdx.test/tools-python/ToolFixture",
    creation_info=creation_info_fixture(),
    name="name_tool",
    summary="summary_tool",
    description="description_tool",
    comment="comment_tool",
    verified_using=[hash_fixture()],
    external_references=[external_reference_fixture()],
    external_identifier=[external_identifier_fixture()],
    extension=None,
) -> Tool:
    verified_using = [] if verified_using is None else verified_using
    external_references = [] if external_references is None else external_references
    external_identifier = [] if external_identifier is None else external_identifier
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
