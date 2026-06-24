import json
import os
from datetime import datetime, timezone

from semantic_version import Version
from spdx_python_model import v3_0_1 as spdx_3_0

from spdx_tools.spdx3.binding.shacl_to_spdx3_converter import convert_to_payload
from spdx_tools.spdx3.binding.spdx3_to_shacl_converter import Spdx3ToSHACLConverter
from spdx_tools.spdx3.model.agent import Agent
from spdx_tools.spdx3.model.creation_info import CreationInfo
from spdx_tools.spdx3.model.element import Element
from spdx_tools.spdx3.model.individual_elements_ids import NO_ASSERTION_LICENSE_ID
from spdx_tools.spdx3.model.relationship import Relationship, RelationshipType
from spdx_tools.spdx3.model.security.cvss_severity_type import CvssSeverityType
from spdx_tools.spdx3.model.security.cvss_v3_vuln_assessment_relationship import CvssV3VulnAssessmentRelationship
from spdx_tools.spdx3.model.security.exploit_catalog_vuln_assessment_relationship import (
    ExploitCatalogType,
    ExploitCatalogVulnAssessmentRelationship,
)
from spdx_tools.spdx3.model.security.vulnerability import Vulnerability
from spdx_tools.spdx3.model.software.package import Package
from spdx_tools.spdx3.model.spdx_document import SpdxDocument
from spdx_tools.spdx3.payload import Payload
from tests.spdx3.binding.test_domain_model import get_all_domain_classes
from tests.spdx3.fixtures import fixture_factory


def test_serializing_and_compare_it_to_deserialized_spdx():
    file_path = os.path.join(os.path.dirname(__file__), "../data/spdxV3-example.json")
    object_set = spdx_3_0.SHACLObjectSet()
    deserializer = spdx_3_0.JSONLDDeserializer()

    with open(file_path, "r") as fd:
        sbom = json.load(fd)
        deserializer.deserialize_data(sbom, object_set)

    payload = convert_to_payload(object_set)

    # convert back to SHACL and serialize, then compare to original file
    shacl_object_set = convert_to_shacl(payload)

    serializer = spdx_3_0.JSONLDSerializer()
    serialized_data = serializer.serialize_data(shacl_object_set)

    with open(file_path, "r") as fd:
        expected_data = json.load(fd)

    # The creationInfo objects will have different IDs after serialization,
    # so we need to remove them and references to them before comparison
    for item in serialized_data["@graph"]:
        if item.get("type") == "CreationInfo":
            item.pop("@id", None)

    for item in expected_data["@graph"]:
        if item.get("type") == "CreationInfo":
            item.pop("@id", None)

    cleaned_serialized_data = normalize_and_exclude_creation_info(serialized_data)
    cleaned_expected_data = normalize_and_exclude_creation_info(expected_data)

    assert cleaned_serialized_data == cleaned_expected_data


def test_serializing_and_compare_it_to_deserialized_spdx_2():
    file_path = os.path.join(os.path.dirname(__file__), "../data/example6-bin.json")
    object_set = spdx_3_0.SHACLObjectSet()
    deserializer = spdx_3_0.JSONLDDeserializer()

    with open(file_path, "r") as fd:
        sbom = json.load(fd)
        deserializer.deserialize_data(sbom, object_set)

    payload = convert_to_payload(object_set)

    # verify creation info is correct
    creation_info = payload.get_element(
        "https://swinslow.net/spdx-examples/example6/hello-go-bin-v2-specv3/document0"
    ).creation_info
    assert creation_info is not None

    # convert back to SHACL and serialize, then compare to original file
    shacl_object_set = convert_to_shacl(payload)

    serializer = spdx_3_0.JSONLDSerializer()
    serialized_data = serializer.serialize_data(shacl_object_set)

    with open(file_path, "r") as fd:
        expected_data = json.load(fd)

    # The creationInfo objects will have different IDs after serialization,
    # so we need to remove them and references to them before comparison
    for item in serialized_data["@graph"]:
        if item.get("type") == "CreationInfo":
            item.pop("@id", None)

    for item in expected_data["@graph"]:
        if item.get("type") == "CreationInfo":
            item.pop("@id", None)

    cleaned_serialized_data = normalize_and_exclude_creation_info(serialized_data)
    cleaned_expected_data = normalize_and_exclude_creation_info(expected_data)

    assert cleaned_serialized_data == cleaned_expected_data


def remove_creation_info_from_json(obj):
    """Recursively remove 'creationInfo' fields from JSON objects."""
    if isinstance(obj, dict):
        # Create a new dict without 'creationInfo' field
        return {k: remove_creation_info_from_json(v) for k, v in obj.items() if k != "creationInfo"}
    elif isinstance(obj, list):
        return [remove_creation_info_from_json(item) for item in obj]
    else:
        return obj


def normalize_and_exclude_creation_info(obj):
    """Normalize JSON and exclude creationInfo fields."""
    # First remove creationInfo fields
    cleaned_obj = remove_creation_info_from_json(obj)
    # Then normalize for comparison
    return normalize_json(cleaned_obj)


def normalize_json(obj):
    """Recursively normalize JSON object for comparison."""
    if isinstance(obj, dict):
        return {k: normalize_json(v) for k, v in sorted(obj.items())}
    elif isinstance(obj, list):
        # Sort lists if items are comparable
        try:
            return sorted([normalize_json(item) for item in obj], key=str)
        except TypeError:
            # If items can't be sorted, just normalize them
            return [normalize_json(item) for item in obj]
    else:
        return obj


def test_multiple_creation_info_serialization_with_library():
    document_id = "urn:documentid.com/1"
    agent_id = "urn:agentid.com/asd"
    creation_info_id_1 = "_:CreationInfo0"
    creation_info_id_2 = "_:CreationInfo1"

    creation_info1 = CreationInfo(
        Version("3.0.1"), datetime.now().astimezone(timezone.utc), [agent_id], comment="test1"
    )
    creation_info2 = CreationInfo(
        Version("3.0.1"), datetime.now().astimezone(timezone.utc), [agent_id], comment="test2"
    )

    agent = Agent(agent_id, creation_info1)

    document = SpdxDocument(document_id, "Document Name", [], [], creation_info=creation_info2)

    payload = Payload()
    payload.add_element(agent)
    payload.add_element(document)

    converter = Spdx3ToSHACLConverter()
    shacl_set = converter.convert(payload)

    serializer = spdx_3_0.JSONLDSerializer()
    serialized_data = serializer.serialize_data(shacl_set)

    # Extract the graph array from serialized data
    graph = serialized_data.get("@graph", [])

    # Find CreationInfo objects by ID
    graph = serialized_data.get("@graph", [])
    creation_infos = {item.get("@id"): item for item in graph if item.get("type") == "CreationInfo"}

    # Assert both creation infos exist
    assert len(creation_infos) == 2, f"Expected 2 CreationInfo objects, found {len(creation_infos)}"
    assert creation_info_id_1 in creation_infos, f"CreationInfo with ID '{creation_info_id_1}' not found"
    assert creation_info_id_2 in creation_infos, f"CreationInfo with ID '{creation_info_id_2}' not found"

    # The creation infos may have different IDs and be in an arbitrary order, so we need to assign them by comment
    creation_info1_serialized = next((ci for ci in creation_infos.values() if ci.get("comment") == "test1"), None)
    creation_info2_serialized = next((ci for ci in creation_infos.values() if ci.get("comment") == "test2"), None)

    # Assert both creation infos exist in serialized data
    assert (
        creation_info1_serialized is not None
    ), f"CreationInfo with ID '{creation_info_id_1}' not found in serialized data"
    assert (
        creation_info2_serialized is not None
    ), f"CreationInfo with ID '{creation_info_id_2}' not found in serialized data"

    # Assert their properties are correctly serialized
    assert creation_info1_serialized.get("comment") == "test1"
    assert creation_info1_serialized.get("specVersion") == "3.0.1"

    assert creation_info2_serialized.get("comment") == "test2"
    assert creation_info2_serialized.get("specVersion") == "3.0.1"

    # Assert that both have the agent in their createdBy field
    assert agent_id in creation_info1_serialized.get("createdBy")
    assert agent_id in creation_info2_serialized.get("createdBy")

    # Assert that the Agent's reference to CreationInfo is correct
    agent = next((item for item in graph if item.get("type") == "Agent"), None)
    assert agent is not None, "Agent not found in serialized data"
    assert agent.get("creationInfo") == creation_info_id_1

    # Assert that the SpdxDocument's reference to CreationInfo is correct
    spdx_document = next((item for item in graph if item.get("type") == "SpdxDocument"), None)
    assert spdx_document is not None, "SpdxDocument not found in serialized data"
    assert spdx_document.get("creationInfo") == creation_info_id_2


def convert_to_shacl(payload: Payload) -> spdx_3_0.SHACLObjectSet:
    converter = Spdx3ToSHACLConverter()
    return converter.convert(payload)


def test_serializing_and_compare_it_to_deserialized_spdx_3():
    file_path = os.path.join(os.path.dirname(__file__), "../data/appbomination.spdx.json")
    object_set = spdx_3_0.SHACLObjectSet()
    deserializer = spdx_3_0.JSONLDDeserializer()

    with open(file_path, "r") as fd:
        sbom = json.load(fd)
        deserializer.deserialize_data(sbom, object_set)

    payload = convert_to_payload(object_set)

    # verify that the creation infos are linked correctly
    spdx_document = payload.get_element(
        "http://www.sourceauditor.com/spdxdocs/appbomination-src/e3b71037-57de-44c9-8b7f-4e8a62f45311-specv3/document0"
    )
    creation_info_1 = spdx_document.creation_info
    assert creation_info_1 is not None

    package = payload.get_element(
        (
            "http://www.sourceauditor.com/spdxdocs/appbomination-src/"
            "e3b71037-57de-44c9-8b7f-4e8a62f45311-specv3/SPDXRef-gnrtd94"
        )
    )
    creation_info_0 = package.creation_info
    assert creation_info_0 is not None

    assert creation_info_0 != creation_info_1

    software_file = payload.get_element(
        (
            "http://www.sourceauditor.com/spdxdocs/appbomination-src/"
            "e3b71037-57de-44c9-8b7f-4e8a62f45311-specv3/SPDXRef-gnrtd91"
        )
    )
    assert creation_info_0 == software_file.creation_info

    tool = payload.get_element(
        (
            "http://www.sourceauditor.com/spdxdocs/appbomination-src/"
            "e3b71037-57de-44c9-8b7f-4e8a62f45311-specv3/additionalToolSPDXRef-gnrtd72"
        )
    )
    assert creation_info_1 == tool.creation_info

    # convert back to SHACL and serialize, then compare to original file
    shacl_object_set = convert_to_shacl(payload)

    serializer = spdx_3_0.JSONLDSerializer()
    serialized_data = serializer.serialize_data(shacl_object_set)

    with open(file_path, "r") as fd:
        expected_data = json.load(fd)

    # The creationInfo objects will have different IDs after serialization,
    # so we need to remove them and references to them before comparison
    for item in serialized_data["@graph"]:
        if item.get("type") == "CreationInfo":
            item.pop("@id", None)

    # Also, this SPDX file being read has a blank "software_sourceInfo" field, which the SHACL bindings deserialize
    # as a None value, so when serializing it back to JSON-LD it becomes absent.
    # To handle this we remove that field from the expected data as well.
    for item in expected_data["@graph"]:
        if item.get("type") == "CreationInfo":
            item.pop("@id", None)
        if item.get("type") == "software_Package" and "software_sourceInfo" in item:
            item.pop("software_sourceInfo", None)

    cleaned_serialized_data = normalize_and_exclude_creation_info(serialized_data)
    cleaned_expected_data = normalize_and_exclude_creation_info(expected_data)

    assert cleaned_expected_data == cleaned_serialized_data


def test_individual_element_conversion():
    document_id = "urn:documentid.com/1"
    agent_id = "urn:agentid.com/asd"
    package_id = "urn:packageid.com/1"
    relationship_id = "urn:relationshipid.com/1"
    vuln_id = "urn:vulnerabilityid.com/1"
    cvss_relationship_id = "urn:vulnerabilityrelationship.com/1"
    exploit_relationship_id = "urn:exploitrelationship.com/1"

    creation_info1 = CreationInfo(
        Version("3.0.1"), datetime.now().astimezone(timezone.utc), [agent_id], comment="test1"
    )

    agent = Agent(agent_id, creation_info1)

    document = SpdxDocument(document_id, "Document Name", [], [], creation_info=creation_info1)

    package = Package(package_id, "Package Name", creation_info1, built_time=datetime.now().astimezone(timezone.utc))

    relationship = Relationship(
        relationship_id,
        package_id,
        RelationshipType.HAS_CONCLUDED_LICENSE,
        creation_info1,
        to=[NO_ASSERTION_LICENSE_ID],
    )

    vulnerability = Vulnerability(vuln_id, creation_info=creation_info1, name="Vulnerability Name")

    vuln_relationship = CvssV3VulnAssessmentRelationship(
        cvss_relationship_id,
        vuln_id,
        list(package_id),
        RelationshipType.AFFECTS,
        7.5,
        CvssSeverityType.HIGH,
        "CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H/E:P/RL:U/RC:R",
        creation_info1,
    )

    vuln_exploit_catalog_relationship = ExploitCatalogVulnAssessmentRelationship(
        exploit_relationship_id,
        vuln_id,
        RelationshipType.HAS_ASSESSMENT_FOR,
        list(package_id),
        ExploitCatalogType.KEV,
        False,
        "https://www.cisa.gov",
        creation_info1,
    )

    payload = Payload()
    payload.add_element(agent)
    payload.add_element(document)
    payload.add_element(package)
    payload.add_element(relationship)
    payload.add_element(vulnerability)
    payload.add_element(vuln_relationship)
    payload.add_element(vuln_exploit_catalog_relationship)

    converter = Spdx3ToSHACLConverter()
    shacl_set = converter.convert(payload)

    serializer = spdx_3_0.JSONLDSerializer()
    serialized_data = serializer.serialize_data(shacl_set)

    serialized_relationship = next(
        (item for item in serialized_data.get("@graph", []) if item.get("type") == "Relationship"), None
    )

    assert serialized_relationship is not None, "Relationship not found in serialized data"
    assert serialized_relationship.get("from") == package_id
    assert serialized_relationship.get("to") == ["expandedlicensing_NoAssertionLicense"]


def test_fixture_serialization():
    payload = Payload()

    for domain_class in get_all_domain_classes():
        try:
            fixture = fixture_factory(domain_class)
        except ValueError:
            if isinstance(domain_class, Element) or isinstance(domain_class, CreationInfo):
                raise RuntimeError(f"Domain class: {type(domain_class)} is missing its fixture.")
            else:
                # not in the fixture factory, but isn't a stand alone class, e.g. an enum, so it's okay to skip
                continue
        payload.add_element(fixture)

    converter = Spdx3ToSHACLConverter()
    shacl_set = converter.convert(payload)

    serializer = spdx_3_0.JSONLDSerializer()
    serializer.serialize_data(shacl_set)
