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
    ProfileIdentifierType,
    Relationship,
    RelationshipCompleteness,
    RelationshipType,
    SoftwareAgent,
    SpdxDocument,
    Tool,
)
from spdx_tools.spdx3.model.ai.ai_package import AIPackage, SafetyRiskAssessmentType
from spdx_tools.spdx3.model.build import Build
from spdx_tools.spdx3.model.dataset.dataset import (
    ConfidentialityLevelType,
    Dataset,
    DatasetAvailabilityType,
    DatasetType,
)
from spdx_tools.spdx3.model.licensing import (
    CustomLicense,
    CustomLicenseAddition,
    ListedLicense,
    ListedLicenseException,
)
from spdx_tools.spdx3.model.positive_integer_range import PositiveIntegerRange
from spdx_tools.spdx3.model.security import (
    CvssV2VulnAssessmentRelationship,
    CvssV3VulnAssessmentRelationship,
    EpssVulnAssessmentRelationship,
    ExploitCatalogType,
    ExploitCatalogVulnAssessmentRelationship,
    SsvcDecisionType,
    SsvcVulnAssessmentRelationship,
    VexAffectedVulnAssessmentRelationship,
    VexFixedVulnAssessmentRelationship,
    VexJustificationType,
    VexNotAffectedVulnAssessmentRelationship,
    VexUnderInvestigationVulnAssessmentRelationship,
    Vulnerability,
)
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
) -> CreationInfo:
    created_by = ["https://spdx.test/tools-python/creation_info_created_by"] if created_by is None else created_by
    created_using = (
        ["https://spdx.test/tools-python/creation_info_created_using"] if created_using is None else created_using
    )
    profile = (
        [ProfileIdentifierType.CORE, ProfileIdentifierType.SOFTWARE, ProfileIdentifierType.LICENSING]
        if profile is None
        else profile
    )
    return CreationInfo(
        spec_version=spec_version,
        created=created,
        created_by=created_by,
        profile=profile,
        data_license=data_license,
        created_using=created_using,
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
    defining_document="https://spdx.test/tools-python/defining_document",
) -> ExternalMap:
    verified_using = [hash_fixture()] if verified_using is None else verified_using
    return ExternalMap(
        external_id=external_id,
        verified_using=verified_using,
        location_hint=location_hint,
        defining_document=defining_document,
    )


def namespace_map_fixture(
    prefix="namespaceMapPrefix", namespace="https://spdx.test/tools-python/namespace_map_namespace"
) -> NamespaceMap:
    return NamespaceMap(prefix=prefix, namespace=namespace)


def listed_license_fixture(
    license_id="https://spdx.test/tools-python/license_id",
    license_name="license name",
    license_text="license text",
    license_comment="license comment",
    see_also=None,
    is_osi_approved=True,
    is_fsf_libre=True,
    standard_license_header="license header",
    standard_license_template="license template",
    is_deprecated_license_id=True,
    obsoleted_by="https://spdx.test/tools-python/obsoleted_by_license_id",
    list_version_added="2.1",
    deprecated_version="2.2",
):
    see_also = ["https://see.also/license"] if see_also is None else see_also
    return ListedLicense(
        license_id=license_id,
        license_name=license_name,
        license_text=license_text,
        license_comment=license_comment,
        see_also=see_also,
        is_osi_approved=is_osi_approved,
        is_fsf_libre=is_fsf_libre,
        standard_license_header=standard_license_header,
        standard_license_template=standard_license_template,
        is_deprecated_license_id=is_deprecated_license_id,
        obsoleted_by=obsoleted_by,
        list_version_added=list_version_added,
        deprecated_version=deprecated_version,
    )


ELEMENT_DICT = {
    "spdx_id": "https://spdx.test/tools-python/element_fixture",
    "creation_info": creation_info_fixture(),
    "name": "elementName",
    "summary": "elementSummary",
    "description": "elementDescription",
    "comment": "elementComment",
    "verified_using": [hash_fixture()],
    "external_reference": [external_reference_fixture()],
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

LICENSE_DICT = {
    "license_id": "https://spdx.test/tools-python/license_id",
    "license_name": "license name",
    "license_text": "license text",
    "license_comment": "license comment",
    "see_also": ["https://see.also/license"],
    "is_osi_approved": True,
    "is_fsf_libre": True,
    "standard_license_header": "license header",
    "standard_license_template": "license template",
    "is_deprecated_license_id": True,
    "obsoleted_by": "https://spdx.test/tools-python/obsoleted_by_license_id",
}

LISTED_LICENSE_DICT = {
    "list_version_added": "2.1",
    "deprecated_version": "2.2",
}

LICENSE_ADDITION_DICT = {
    "addition_id": "https://spdx.test/tools-python/addition_id",
    "addition_name": "addition name",
    "addition_text": "addition text",
    "addition_comment": "addition comment",
    "see_also": ["https://see.also/addition"],
    "standard_addition_template": "addition template",
    "is_deprecated_addition_id": True,
    "obsoleted_by": "https://spdx.test/tools-python/obsoleted_by_addition_id",
}

LISTED_LICENSE_EXCEPTION_DICT = {
    "list_version_added": "2.1",
    "deprecated_version": "2.2",
}

VULNERABILITY_DICT = {
    "published_time": datetime(2010, 1, 1),
    "modified_time": datetime(2011, 1, 1),
    "withdrawn_time": datetime(2012, 1, 1),
}

VULN_ASSESSMENT_RELATIONSHIP_DICT = {
    "assessed_element": "https://spdx.test/tools-python/assessed_element",
    "published_time": datetime(2004, 1, 1),
    "supplied_by": "https://spdx.test/tools-python/supplied_by",
    "modified_time": datetime(2005, 1, 1),
    "withdrawn_time": datetime(2006, 1, 1),
}

CVSS_V2_VULN_ASSESSMENT_RELATIONSHIP_DICT = {
    "score": "4.3",
    "severity": "low",
    "vector": "(AV:N/AC:M/Au:N/C:P/I:N/A:N)",
    "relationship_type": RelationshipType.HAS_ASSESSMENT_FOR,
}

CVSS_V3_VULN_ASSESSMENT_RELATIONSHIP_DICT = {
    "score": "6.8",
    "severity": "medium",
    "vector": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:N/A:N",
    "relationship_type": RelationshipType.HAS_ASSESSMENT_FOR,
}

EPSS_VULN_ASSESSMENT_RELATIONSHIP_DICT = {
    "probability": 80,
    "severity": "high",
    "relationship_type": RelationshipType.HAS_ASSESSMENT_FOR,
}

SSVC_VULN_ASSESSMENT_RELATIONSHIP_DICT = {
    "decision_type": SsvcDecisionType.ACT,
    "relationship_type": RelationshipType.HAS_ASSESSMENT_FOR,
}

EXPLOIT_CATALOG_VULN_ASSESSMENT_RELATIONSHIP_DICT = {
    "catalog_type": ExploitCatalogType.KEV,
    "exploited": True,
    "locator": "https://www.cisa.gov/known-exploited-vulnerabilities-catalog",
    "relationship_type": RelationshipType.HAS_ASSESSMENT_FOR,
}

VEX_VULN_ASSESSMENT_RELATIONSHIP_DICT = {
    "vex_version": "v4.2",
    "status_notes": "some status notes",
}

VEX_AFFECTED_VULN_ASSESSMENT_RELATIONSHIP_DICT = {
    "action_statement": "Upgrade to version 1.4 of ACME application.",
    "action_statement_time": [datetime(2015, 10, 15)],
    "relationship_type": RelationshipType.AFFECTS,
}

VEX_NOT_AFFECTED_VULN_ASSESSMENT_RELATIONSHIP_DICT = {
    "justification_type": VexJustificationType.COMPONENT_NOT_PRESENT,
    "impact_statement": "Not using this vulnerable part of this library.",
    "impact_statement_time": datetime(2015, 10, 15),
    "relationship_type": RelationshipType.DOES_NOT_AFFECT,
}

VEX_UNDER_INVESTIGATION_VULN_ASSESSMENT_RELATIONSHIP_DICT = {
    "relationship_type": RelationshipType.UNDER_INVESTIGATION_FOR,
}

VEX_FIXED_VULN_ASSESSMENT_RELATIONSHIP_DICT = {
    "relationship_type": RelationshipType.FIXED_IN,
}

AIPACKAGE_DICT = {
    "energy_consumption": "energyConsumption",
    "standard_compliance": ["standardCompliance"],
    "limitation": "aIPackageLimitation",
    "type_of_model": ["typeOfModel"],
    "information_about_training": "informationAboutTraining",
    "information_about_application": "informationAboutApplication",
    "hyperparameter": {"aIPackageHypParaKey": "aIPackageHypParaValue"},
    "model_data_preprocessing": ["aImodelDataPreprocessing"],
    "model_explainability": ["aImodelExplainability"],
    "sensitive_personal_information": True,
    "metric_decision_threshold": {"metricDecisionThresholdKey": "metricDecisionThresholdValue"},
    "metric": {"aIMetricKey": "aIMetricValue"},
    "domain": ["aIDomain"],
    "autonomy_type": True,
    "safety_risk_assessment": SafetyRiskAssessmentType.LOW,
}

ARTIFACT_DICT = {
    "originated_by": ["https://spdx.test/tools-python/originatedBy"],
    "supplied_by": ["https://spdx.test/tools-python/suppliedBy"],
    "built_time": datetime(2004, 1, 1),
    "release_time": datetime(2005, 1, 1),
    "valid_until_time": datetime(2006, 1, 1),
    "standard": ["https://spdx.test/tools-python/standard"],
}

SOFTWARE_ARTIFACT_DICT = {
    "content_identifier": "https://spdx.test/tools-python/contentIdentifier",
    "primary_purpose": SoftwarePurpose.SOURCE,
    "additional_purpose": [SoftwarePurpose.OTHER],
    "concluded_license": listed_license_fixture(),
    "declared_license": listed_license_fixture(),
    "copyright_text": "copyrightText",
    "attribution_text": "attributionText",
}

FILE_DICT = {"content_type": "fileContentType"}

PACKAGE_DICT = {
    "package_version": "packageVersion",
    "download_location": "https://spdx.test/tools-python/downloadPackage",
    "package_url": "https://spdx.test/tools-python/package",
    "homepage": "https://spdx.test/tools-python/homepage",
    "source_info": "sourceInfo",
}

SNIPPET_DICT = {"byte_range": PositiveIntegerRange(1024, 2048), "line_range": PositiveIntegerRange(1, 4)}

SOFTWARE_DEPENDENCY_RELATIONSHIP_DICT = {
    "software_linkage": SoftwareDependencyLinkType.OTHER,
    "conditionality": DependencyConditionalityType.OTHER,
}

DATASET_DICT = {
    "dataset_type": [DatasetType.OTHER],
    "data_collection_process": "DatasetDataCollectionProcess",
    "intended_use": "DatasetIntendedUse",
    "dataset_size": 10,
    "dataset_noise": "DatasetNoise",
    "data_preprocessing": ["DataPreprocessing"],
    "sensor": {"SensorKey": "SensorValue"},
    "known_bias": ["DatasetKnownBias"],
    "sensitive_personal_information": True,
    "anonymization_method_used": ["DatasetAnonymizationMethodUsed"],
    "confidentiality_level": ConfidentialityLevelType.CLEAR,
    "dataset_update_mechanism": "DatasetUpdateMechanism",
    "dataset_availability": DatasetAvailabilityType.QUERY,
}

BUILD_DICT = {
    "build_type": "BuildType",
    "build_id": "BuildId",
    "config_source_entrypoint": ["ConfigSourceEntrypoint"],
    "config_source_uri": ["ConfigSourceURI"],
    "config_source_digest": [hash_fixture()],
    "parameters": {"parameter": "value"},
    "build_start_time": datetime(2015, 4, 4),
    "build_end_time": datetime(2015, 4, 5),
    "environment": {"environment_param": "environment_value"},
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
    ListedLicense: [LICENSE_DICT, LISTED_LICENSE_DICT],
    CustomLicense: [LICENSE_DICT],
    ListedLicenseException: [LICENSE_ADDITION_DICT, LISTED_LICENSE_EXCEPTION_DICT],
    CustomLicenseAddition: [LICENSE_ADDITION_DICT],
    CvssV2VulnAssessmentRelationship: [
        ELEMENT_DICT,
        RELATIONSHIP_DICT,
        VULN_ASSESSMENT_RELATIONSHIP_DICT,
        CVSS_V2_VULN_ASSESSMENT_RELATIONSHIP_DICT,
    ],
    CvssV3VulnAssessmentRelationship: [
        ELEMENT_DICT,
        RELATIONSHIP_DICT,
        VULN_ASSESSMENT_RELATIONSHIP_DICT,
        CVSS_V3_VULN_ASSESSMENT_RELATIONSHIP_DICT,
    ],
    EpssVulnAssessmentRelationship: [
        ELEMENT_DICT,
        RELATIONSHIP_DICT,
        VULN_ASSESSMENT_RELATIONSHIP_DICT,
        EPSS_VULN_ASSESSMENT_RELATIONSHIP_DICT,
    ],
    ExploitCatalogVulnAssessmentRelationship: [
        ELEMENT_DICT,
        RELATIONSHIP_DICT,
        VULN_ASSESSMENT_RELATIONSHIP_DICT,
        EXPLOIT_CATALOG_VULN_ASSESSMENT_RELATIONSHIP_DICT,
    ],
    SsvcVulnAssessmentRelationship: [
        ELEMENT_DICT,
        RELATIONSHIP_DICT,
        VULN_ASSESSMENT_RELATIONSHIP_DICT,
        SSVC_VULN_ASSESSMENT_RELATIONSHIP_DICT,
    ],
    VexAffectedVulnAssessmentRelationship: [
        ELEMENT_DICT,
        RELATIONSHIP_DICT,
        VULN_ASSESSMENT_RELATIONSHIP_DICT,
        VEX_VULN_ASSESSMENT_RELATIONSHIP_DICT,
        VEX_AFFECTED_VULN_ASSESSMENT_RELATIONSHIP_DICT,
    ],
    VexFixedVulnAssessmentRelationship: [
        ELEMENT_DICT,
        RELATIONSHIP_DICT,
        VULN_ASSESSMENT_RELATIONSHIP_DICT,
        VEX_VULN_ASSESSMENT_RELATIONSHIP_DICT,
        VEX_FIXED_VULN_ASSESSMENT_RELATIONSHIP_DICT,
    ],
    VexNotAffectedVulnAssessmentRelationship: [
        ELEMENT_DICT,
        RELATIONSHIP_DICT,
        VULN_ASSESSMENT_RELATIONSHIP_DICT,
        VEX_VULN_ASSESSMENT_RELATIONSHIP_DICT,
        VEX_NOT_AFFECTED_VULN_ASSESSMENT_RELATIONSHIP_DICT,
    ],
    VexUnderInvestigationVulnAssessmentRelationship: [
        ELEMENT_DICT,
        RELATIONSHIP_DICT,
        VULN_ASSESSMENT_RELATIONSHIP_DICT,
        VEX_VULN_ASSESSMENT_RELATIONSHIP_DICT,
        VEX_UNDER_INVESTIGATION_VULN_ASSESSMENT_RELATIONSHIP_DICT,
    ],
    Vulnerability: [ELEMENT_DICT, VULNERABILITY_DICT],
    AIPackage: [AIPACKAGE_DICT, PACKAGE_DICT, ELEMENT_DICT, ARTIFACT_DICT, SOFTWARE_ARTIFACT_DICT],
    File: [ELEMENT_DICT, ARTIFACT_DICT, SOFTWARE_ARTIFACT_DICT, FILE_DICT],
    Package: [ELEMENT_DICT, ARTIFACT_DICT, SOFTWARE_ARTIFACT_DICT, PACKAGE_DICT],
    Snippet: [ELEMENT_DICT, ARTIFACT_DICT, SOFTWARE_ARTIFACT_DICT, SNIPPET_DICT],
    SoftwareDependencyRelationship: [
        ELEMENT_DICT,
        RELATIONSHIP_DICT,
        LIFECYCLE_SCOPED_RELATIONSHIP_DICT,
        SOFTWARE_DEPENDENCY_RELATIONSHIP_DICT,
    ],
    Dataset: [ELEMENT_DICT, ARTIFACT_DICT, SOFTWARE_ARTIFACT_DICT, PACKAGE_DICT, DATASET_DICT],
    Build: [ELEMENT_DICT, BUILD_DICT],
}


def fixture_factory(clazz: Type[Any], **kwargs) -> Any:
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

    if "spdx_id" in fixture_dict.keys():
        fixture_dict["spdx_id"] = f"https://spdx.test/tools-python/{clazz.__name__}_fixture"

    return fixture_dict
