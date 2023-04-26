# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import json

# current workflow: markdown files + spec_parser -> model.ttl -> convert to json_ld: SPDX_OWL.json -> use the function below (needs to be fixed) to generate context.json
# TODO: Enums should look like this:
# "annotationType": {
#     "@id": "core:annotationType",
#     "@type": "@vocab",
#     "@context": {
#         "@vocab": "core:AnnotationType#"   <- or "/" at the end, who knows
#     }
# },

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
            context_dict[name] = {"@id": node["@id"], "@type": node["rdfs:range"]["@id"]}

        elif node_type == "owl:Class":
            name = node["@id"].split(":")[-1]
            context_dict[name] = node["@id"]

        elif isinstance(node_type, list):
            name = node["@id"].split(":")[-1]
            context_dict[name] = node["@id"]

        else:
            print(f"unknown node_type: {node_type}")

    with open("src/spdx_tools/spdx3/writer/json_ld/context.json", "w") as infile:
        json.dump(context_dict, infile)
