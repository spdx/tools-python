# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import json
import os.path

# current workflow: markdown files + spec_parser -> model.ttl -> convert to json_ld: SPDX_OWL.json ->
# use the function below to generate context.json
# properties with Enum range should look like this (probably), so that their values are automatically appended
# with the Enum URI:
# "annotationType": {
#     "@id": "core:annotationType",
#     "@type": "@vocab",
#     "@context": {
#         "@vocab": "core:AnnotationType/"
#     }
# },

PROPERTIES_WITH_ENUM_RANGE = [
    "safetyRiskAssessment",
    "sensitivePersonalInformation",
    "annotationType",
    "externalIdentifierType",
    "externalReferenceType",
    "algorithm",
    "scope",
    "profile",
    "completeness",
    "relationshipType",
    "confidentialityLevel",
    "datasetAvailability",
    "decisionType",
    "justificationType",
    "catalogType",
    "conditionality",
    "sbomType",
    "softwareLinkage",
    "purpose",
]

REFERENCE_PROPERTY_TYPES = [
    "core:Element",
    "core:Agent",
]


def convert_spdx_owl_to_jsonld_context(spdx_owl: str = "SPDX_OWL.json"):
    with open(spdx_owl, "r") as infile:
        owl_dict = json.load(infile)

    context_dict = owl_dict["@context"]

    for node in owl_dict["@graph"]:
        # print(node)
        node_type = node.get("@type")
        if not node_type:
            # print(node)
            continue

        if "owl:NamedIndividual" in node_type:
            continue
        elif node_type in ["owl:DatatypeProperty", "owl:ObjectProperty"]:
            name = node["@id"].split(":")[-1]
            type_id = node["rdfs:range"]["@id"]

            if name in context_dict and context_dict[name]["@id"].startswith("core"):
                # if in doubt, prioritize core properties
                continue

            if name in PROPERTIES_WITH_ENUM_RANGE:
                if name == "profile":
                    # FIXME: since the allowed values for the profile enum collide with
                    # our namespaces, we need to explicitly remap their meaning in the context
                    context_dict[name] = {
                        "@id": node["@id"],
                        "@type": "@vocab",
                        "@context": {
                            "core": "https://spdx.org/rdf/Core/ProfileIdentifierType/core",
                            "software": "https://spdx.org/rdf/Core/ProfileIdentifierType/software",
                            "licensing": "https://spdx.org/rdf/Core/ProfileIdentifierType/licensing",
                            "security": "https://spdx.org/rdf/Core/ProfileIdentifierType/security",
                            "build": "https://spdx.org/rdf/Core/ProfileIdentifierType/build",
                            "ai": "https://spdx.org/rdf/Core/ProfileIdentifierType/ai",
                            "dataset": "https://spdx.org/rdf/Core/ProfileIdentifierType/dataset",
                            "usage": "https://spdx.org/rdf/Core/ProfileIdentifierType/usage",
                            "extension": "https://spdx.org/rdf/Core/ProfileIdentifierType/extension",
                        },
                    }
                else:
                    context_dict[name] = {
                        "@id": node["@id"],
                        "@type": "@vocab",
                        "@context": {"@vocab": type_id + "/"},
                    }
            elif node_type == "owl:ObjectProperty" and type_id in REFERENCE_PROPERTY_TYPES:
                context_dict[name] = {"@id": node["@id"], "@type": "@id"}
            else:
                context_dict[name] = {"@id": node["@id"], "@type": type_id}

        elif node_type == "owl:Class":
            name = node["@id"].split(":")[-1]
            context_dict[name] = node["@id"]

        elif isinstance(node_type, list):
            name = node["@id"].split(":")[-1]
            context_dict[name] = node["@id"]

        else:
            print(f"unknown node_type: {node_type}")

    with open(os.path.join(os.path.dirname(__file__), "context.json"), "w") as infile:
        json.dump(context_dict, infile)


if __name__ == "__main__":
    convert_spdx_owl_to_jsonld_context("SPDX_OWL.json")
