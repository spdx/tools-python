# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import os

import pytest
from rdflib import RDF, Graph

from spdx_tools.spdx.parser.rdf.extracted_licensing_info_parser import parse_extracted_licensing_info
from spdx_tools.spdx.rdfschema.namespace import SPDX_NAMESPACE


@pytest.mark.parametrize(
    "license_id, extracted_text, comment, license_name, cross_references",
    [
        (
            "LicenseRef-1",
            "extractedText",
            "licenseComment",
            "licenseName",
            ["https://see.also"],
        ),
        (
            "LicenseRef-2",
            "extractedText",
            "licenseComment",
            "another license",
            ["https://see.also"],
        ),
    ],
)
# In rdf, as a short form, the explicit node for licenseId can be omitted, since the ID is also encoded in the URIRef
# of the ExtractedLicensingInfo node. The first test case has an explicit licenseId node whereas the second test case
# does not. This behaviour is similar to the externalDocumentRefId, see the discussion here:
# https://github.com/spdx/spdx-spec/issues/816
def test_parse_extracted_licensing_info(license_id, extracted_text, comment, license_name, cross_references):
    graph = Graph().parse(os.path.join(os.path.dirname(__file__), "data/file_to_test_rdf_parser.rdf.xml"))
    doc_namespace = "https://some.namespace"
    extracted_licensing_info_node = get_extracted_licensing_info_node_by_license_id(graph, license_id)

    extracted_licensing_info = parse_extracted_licensing_info(extracted_licensing_info_node, graph, doc_namespace)

    assert extracted_licensing_info.license_id == license_id
    assert extracted_licensing_info.extracted_text == extracted_text
    assert extracted_licensing_info.comment == comment
    assert extracted_licensing_info.license_name == license_name
    assert extracted_licensing_info.cross_references == cross_references


def get_extracted_licensing_info_node_by_license_id(graph, license_id):
    for extracted_licensing_info_node, _, _ in graph.triples((None, RDF.type, SPDX_NAMESPACE.ExtractedLicensingInfo)):
        if extracted_licensing_info_node.fragment == license_id:
            return extracted_licensing_info_node
