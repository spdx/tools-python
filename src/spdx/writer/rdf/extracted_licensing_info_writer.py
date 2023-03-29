# Copyright (c) 2023 spdx contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from rdflib import Graph, URIRef, RDF, BNode, RDFS, Literal
from spdx.writer.rdf.writer_utils import add_optional_literal, add_literal_or_no_assertion
from spdx.rdfschema.namespace import SPDX_NAMESPACE

from spdx.model.extracted_licensing_info import ExtractedLicensingInfo


def add_extracted_licensing_info_to_graph(extracted_licensing_info: ExtractedLicensingInfo, graph: Graph, doc_node,
                                          doc_namespace: str):
    if extracted_licensing_info.license_id:
        extracted_licensing_info_resource = URIRef(f"{doc_namespace}#{extracted_licensing_info.license_id}")
        graph.add((extracted_licensing_info_resource, RDF.type, SPDX_NAMESPACE.ExtractedLicensingInfo))
    else:
        extracted_licensing_info_resource = BNode()
    add_optional_literal(extracted_licensing_info.license_id, graph, extracted_licensing_info_resource,
                         SPDX_NAMESPACE.licenseId)
    add_optional_literal(extracted_licensing_info.extracted_text, graph, extracted_licensing_info_resource,
                         SPDX_NAMESPACE.extractedText)
    add_literal_or_no_assertion(extracted_licensing_info.license_name, graph, extracted_licensing_info_resource,
                                SPDX_NAMESPACE.name)
    for cross_reference in extracted_licensing_info.cross_references:
        graph.add((extracted_licensing_info_resource, RDFS.seeAlso, Literal(cross_reference)))
    add_optional_literal(extracted_licensing_info.comment, graph, extracted_licensing_info_resource, RDFS.comment)

    graph.add((doc_node, SPDX_NAMESPACE.hasExtractedLicensingInfo, extracted_licensing_info_resource))
