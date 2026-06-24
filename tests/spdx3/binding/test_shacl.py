import json
import os
from datetime import datetime, timezone

from spdx_python_model import v3_0_1 as spdx_3_0


def test_single_creation_info_serialization():
    agent_id = "urn:agentid.com/asd"
    starting_creation_info_id = "_:creationinfo"
    expected_creation_info_id = "_:CreationInfo0"  # The SHACL bindings will rename the ID to this format

    creation_info1 = spdx_3_0.CreationInfo()
    creation_info1.comment = "test"
    creation_info1.specVersion = "3.0.1"
    creation_info1.created = datetime.now().astimezone(timezone.utc)
    creation_info1["@id"] = starting_creation_info_id

    agent = spdx_3_0.Agent()
    agent["@id"] = agent_id
    agent.creationInfo = creation_info1
    creation_info1.createdBy.append(agent)

    document = spdx_3_0.SpdxDocument()
    document.creationInfo = creation_info1
    document["@id"] = "urn:documentid.com/1"

    shacl_set = spdx_3_0.SHACLObjectSet()
    shacl_set.add(creation_info1)
    shacl_set.add(agent)
    shacl_set.add(document)

    serializer = spdx_3_0.JSONLDSerializer()
    serialized_data = serializer.serialize_data(shacl_set)

    # Extract the graph array from serialized data
    graph = serialized_data.get("@graph", [])

    # Find CreationInfo objects by ID
    graph = serialized_data.get("@graph", [])
    creation_infos = {item.get("@id"): item for item in graph if item.get("type") == "CreationInfo"}

    # Assert both creation infos exist
    assert len(creation_infos) == 1, f"Expected 1 CreationInfo objects, found {len(creation_infos)}"
    assert expected_creation_info_id in creation_infos, f"CreationInfo with ID '{expected_creation_info_id}' not found"

    # Assert that the SpdxDocument's reference to CreationInfo is correct
    spdx_document = next((item for item in graph if item.get("type") == "SpdxDocument"), None)
    assert spdx_document is not None, "SpdxDocument not found in serialized data"
    assert (
        spdx_document.get("creationInfo") == expected_creation_info_id
    ), f"SpdxDocument's creationInfo does not reference '{expected_creation_info_id}'"


def test_multiple_creation_info_serialization_no_library():
    agent_id = "urn:agentid.com/asd"
    creation_info_id_1 = "_:CreationInfo1"
    creation_info_id_2 = "_:CreationInfo0"

    creation_info1 = spdx_3_0.CreationInfo()
    creation_info1.comment = "test"
    creation_info1.specVersion = "3.0.1"
    creation_info1.created = datetime.now().astimezone(timezone.utc)
    creation_info1["@id"] = creation_info_id_1

    creation_info2 = spdx_3_0.CreationInfo()
    creation_info2.comment = "test2"
    creation_info2.specVersion = "3.0.1"
    creation_info2.created = datetime.now().astimezone(timezone.utc)
    creation_info1.createdBy.append(agent_id)
    creation_info2["@id"] = creation_info_id_2

    agent = spdx_3_0.Agent()
    agent["@id"] = agent_id
    agent.creationInfo = creation_info1
    creation_info1.createdBy.append(agent_id)
    creation_info2.createdBy.append(agent_id)

    document = spdx_3_0.SpdxDocument()
    document.creationInfo = creation_info2
    document["@id"] = "urn:documentid.com/1"

    shacl_set = spdx_3_0.SHACLObjectSet()
    shacl_set.add(creation_info1)
    shacl_set.add(creation_info2)
    shacl_set.add(agent)
    shacl_set.add(document)

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

    # The creation infos will have different IDs and be in an arbitrary order, so we need to assign them by comment
    creation_info1_serialized = next((ci for ci in creation_infos.values() if ci.get("comment") == "test"), None)
    creation_info2_serialized = next((ci for ci in creation_infos.values() if ci.get("comment") == "test2"), None)

    # Assert both creation infos exist in serialized data
    assert (
        creation_info1_serialized is not None
    ), f"CreationInfo with ID '{creation_info_id_1}' not found in serialized data"
    assert (
        creation_info2_serialized is not None
    ), f"CreationInfo with ID '{creation_info_id_2}' not found in serialized data"

    # Assert their properties are correctly serialized
    assert creation_info1_serialized.get("comment") == "test"
    assert creation_info1_serialized.get("specVersion") == "3.0.1"

    assert creation_info2_serialized.get("comment") == "test2"
    assert creation_info2_serialized.get("specVersion") == "3.0.1"

    # Assert that both have the agent in their createdBy field
    assert agent_id in creation_info1_serialized.get("createdBy", [])
    assert agent_id in creation_info2_serialized.get("createdBy", [])


def test_that_spdx_python_tools_is_importing_creation_info_ids_wrong():
    file_path = os.path.join(os.path.dirname(__file__), "../data/spdxV3-example.json")
    object_set = spdx_3_0.SHACLObjectSet()
    deserializer = spdx_3_0.JSONLDDeserializer()

    with open(file_path, "r") as fd:
        sbom = json.load(fd)
        deserializer.deserialize_data(sbom, object_set)

    serializer = spdx_3_0.JSONLDSerializer()
    serialized_data = serializer.serialize_data(object_set)

    creation_infos = []
    for item in serialized_data["@graph"]:
        if item.get("type") == "CreationInfo":
            creation_infos.append(item)

    assert len(creation_infos) == 1
    creation_info = creation_infos[0]
    assert (
        creation_info["@id"] != "_:creationinfo"
    )  # This is the ID that was in the original file, but the SHACL bindings rename it to the following format instead
    assert creation_info["@id"] == "_:CreationInfo0"


def test_that_individual_element_uri_conversion_works():
    spdx = """
    {
    "@context": "https://spdx.org/rdf/3.0.1/spdx-context.jsonld",
    "@graph": [
        {
        "type": "CreationInfo",
        "@id": "_:CreationInfo0",
        "comment": "test",
        "created": "2025-10-15T01:02:01Z",
        "createdBy": [
            "urn:agentid.com/asd"
        ],
        "specVersion": "3.0.1"
        },
        {
        "type": "Agent",
        "spdxId": "urn:agentid.com/asd",
        "creationInfo": "_:CreationInfo0"
        },
        {
        "type": "SpdxDocument",
        "spdxId": "urn:documentid.com/1",
        "creationInfo": "_:CreationInfo0"
        },
    {
      "type": "Relationship",
      "spdxId": "urn:relationshipid.com/1",
      "creationInfo": "_:CreationInfo0",
      "from": "https://spdx.org/rdf/3.0.1/terms/Core/NoneElement",
      "relationshipType": "hasConcludedLicense",
      "to": [
        "https://spdx.org/rdf/3.0.1/terms/ExpandedLicensing/NoAssertionLicense"
      ]
    }
    ]
    }
    """
    object_set = spdx_3_0.SHACLObjectSet()
    deserializer = spdx_3_0.JSONLDDeserializer()

    deserializer.deserialize_data(json.loads(spdx), object_set)

    serializer = spdx_3_0.JSONLDSerializer()
    serialized_data = serializer.serialize_data(object_set)

    graph = serialized_data.get("@graph", [])
    relationship = next((item for item in graph if item.get("type") == "Relationship"), None)
    assert relationship is not None
    assert relationship.get("from") == "NoneElement"
    assert "expandedlicensing_NoAssertionLicense" in relationship.get("to")
