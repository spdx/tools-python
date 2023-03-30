# SPDX-FileCopyrightText: 2023 spdx contributors

# SPDX-License-Identifier: Apache-2.0
import os

from rdflib import RDF, Graph

from spdx.parser.rdf.extracted_licensing_info_parser import parse_extracted_licensing_info
from spdx.rdfschema.namespace import SPDX_NAMESPACE


def test_parse_extracted_licensing_info():
    graph = Graph().parse(os.path.join(os.path.dirname(__file__), "data/file_to_test_rdf_parser.rdf.xml"))
    doc_node = graph.value(predicate=RDF.type, object=SPDX_NAMESPACE.SpdxDocument)
    extracted_licensing_info_node = graph.value(subject=doc_node, predicate=SPDX_NAMESPACE.hasExtractedLicensingInfo)

    extracted_licensing_info = parse_extracted_licensing_info(extracted_licensing_info_node, graph)

    assert extracted_licensing_info.license_id == "LicenseRef-1"
    assert extracted_licensing_info.extracted_text == "extractedText"
    assert extracted_licensing_info.comment == "licenseComment"
    assert extracted_licensing_info.license_name == "licenseName"
    assert extracted_licensing_info.cross_references == ["https://see.also"]
