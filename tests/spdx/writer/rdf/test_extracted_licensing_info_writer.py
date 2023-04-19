# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from rdflib import RDF, RDFS, Graph, Literal, URIRef

from spdx_tools.spdx.rdfschema.namespace import SPDX_NAMESPACE
from spdx_tools.spdx.writer.rdf.extracted_licensing_info_writer import add_extracted_licensing_info_to_graph
from tests.spdx.fixtures import extracted_licensing_info_fixture


def test_add_extracted_licensing_info_to_graph():
    graph = Graph()
    extracted_licensing_info = extracted_licensing_info_fixture()

    add_extracted_licensing_info_to_graph(extracted_licensing_info, graph, URIRef("docNode"), "docNamespace")

    assert (URIRef("docNode"), SPDX_NAMESPACE.hasExtractedLicensingInfo, None) in graph
    assert (URIRef("docNamespace#LicenseRef-1"), RDF.type, SPDX_NAMESPACE.ExtractedLicensingInfo) in graph
    assert (None, SPDX_NAMESPACE.licenseId, Literal(extracted_licensing_info.license_id)) in graph
    assert (None, SPDX_NAMESPACE.extractedText, Literal(extracted_licensing_info.extracted_text)) in graph
    assert (None, RDFS.seeAlso, Literal(extracted_licensing_info.cross_references[0])) in graph
    assert (None, SPDX_NAMESPACE.name, Literal(extracted_licensing_info.license_name)) in graph
    assert (None, RDFS.comment, Literal(extracted_licensing_info.comment)) in graph
