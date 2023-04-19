# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from rdflib import RDF, RDFS, BNode, Graph, Literal, URIRef

from spdx_tools.spdx.model import ExtractedLicensingInfo
from spdx_tools.spdx.rdfschema.namespace import SPDX_NAMESPACE
from spdx_tools.spdx.writer.rdf.writer_utils import add_literal_or_no_assertion, add_optional_literal


def add_extracted_licensing_info_to_graph(
    extracted_licensing_info: ExtractedLicensingInfo, graph: Graph, doc_node, doc_namespace: str
):
    if extracted_licensing_info.license_id:
        extracted_licensing_info_resource = URIRef(f"{doc_namespace}#{extracted_licensing_info.license_id}")
        graph.add((extracted_licensing_info_resource, RDF.type, SPDX_NAMESPACE.ExtractedLicensingInfo))
    else:
        extracted_licensing_info_resource = BNode()
    add_optional_literal(
        extracted_licensing_info.license_id, graph, extracted_licensing_info_resource, SPDX_NAMESPACE.licenseId
    )
    add_optional_literal(
        extracted_licensing_info.extracted_text, graph, extracted_licensing_info_resource, SPDX_NAMESPACE.extractedText
    )
    add_literal_or_no_assertion(
        extracted_licensing_info.license_name, graph, extracted_licensing_info_resource, SPDX_NAMESPACE.name
    )
    for cross_reference in extracted_licensing_info.cross_references:
        graph.add((extracted_licensing_info_resource, RDFS.seeAlso, Literal(cross_reference)))
    add_optional_literal(extracted_licensing_info.comment, graph, extracted_licensing_info_resource, RDFS.comment)

    graph.add((doc_node, SPDX_NAMESPACE.hasExtractedLicensingInfo, extracted_licensing_info_resource))
