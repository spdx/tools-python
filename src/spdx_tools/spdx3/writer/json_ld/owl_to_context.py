# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import json

# current workflow: markdown files + spec_parser -> model.ttl -> convert to json_ld: SPDX_OWL.json -> use the function below to generate context.json
# properties with Enum range should look like this (probably), so that their values are automatically appended with the Enum URI:
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

def convert_spdx_owl_to_jsonld_context():
    with open("SPDX_OWL.json", "r") as infile:
        owl_dict = json.load(infile)

    context_dict = {
        "core": "https://spdx.org/rdf/Core/",
        "software": "https://spdx.org/rdf/Software/",
        "xsd": "http://www.w3.org/2001/XMLSchema/",
    }

    for node in owl_dict["@graph"]:
        print(node)
        node_type = node["@type"]

        if "owl:NamedIndividual" in node_type:
            continue
        elif node_type in ["owl:DatatypeProperty", "owl:ObjectProperty"]:
            name = node["@id"].split(":")[-1]
            if name in PROPERTIES_WITH_ENUM_RANGE:
                context_dict[name]  = {
                    "@id": node["@id"],
                    "@type": "@vocab",
                    "@context": {
                        "@vocab": node["rdfs:range"]["@id"] + "/"
                    }
                }
            else:
                context_dict[name] = {"@id": node["@id"], "@type": node["rdfs:range"]["@id"]}

        elif node_type == "owl:Class":
            name = node["@id"].split(":")[-1]
            context_dict[name] = node["@id"]

        elif isinstance(node_type, list):
            name = node["@id"].split(":")[-1]
            context_dict[name] = node["@id"]

        else:
            print(f"unknown node_type: {node_type}")

    with open("context.json", "w") as infile:
        json.dump(context_dict, infile)


if __name__ == "__main__":
    convert_spdx_owl_to_jsonld_context()
