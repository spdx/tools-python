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
from typing import Dict

from rdflib import Graph, URIRef, Literal, RDF, RDFS

from spdx.model.file import File
from spdx.writer.casing_tools import snake_case_to_camel_case
from spdx.writer.rdf.checksum_writer import add_checksum_information_to_graph
from spdx.writer.rdf.license_expression_writer import add_license_expression_or_none_or_no_assertion
from spdx.writer.rdf.writer_utils import SPDX_NAMESPACE, add_literal_value, add_namespace_to_spdx_id


def add_file_information_to_graph(file: File, graph: Graph, doc_namespace: str,
                                  external_doc_ref_to_namespace: Dict[str, str]):
    file_resource = URIRef(add_namespace_to_spdx_id(file.spdx_id, doc_namespace, external_doc_ref_to_namespace))
    graph.add((file_resource, RDF.type, SPDX_NAMESPACE.File))
    graph.add((file_resource, SPDX_NAMESPACE.fileName, Literal(file.name)))
    for file_type in file.file_type:
        graph.add((file_resource, SPDX_NAMESPACE.fileType,
                   SPDX_NAMESPACE[f"fileType_{snake_case_to_camel_case(file_type.name)}"]))

    for checksum in file.checksums:
        add_checksum_information_to_graph(checksum, graph, file_resource)

    add_license_expression_or_none_or_no_assertion(graph, file_resource, SPDX_NAMESPACE.licenseConcluded,
                                                   file.license_concluded, doc_namespace)
    add_license_expression_or_none_or_no_assertion(graph, file_resource, SPDX_NAMESPACE.licenseInfoInFile,
                                                   file.license_info_in_file, doc_namespace)

    add_literal_value(graph, file_resource, SPDX_NAMESPACE.licenseComments, file.license_comment)
    add_literal_value(graph, file_resource, SPDX_NAMESPACE.copyrightText, file.copyright_text)
    add_literal_value(graph, file_resource, RDFS.comment, file.comment)
    add_literal_value(graph, file_resource, SPDX_NAMESPACE.noticeText, file.notice)
    for contributor in file.contributors:
        graph.add((file_resource, SPDX_NAMESPACE.fileContributor, Literal(contributor)))
    for attribution_text in file.attribution_texts:
        graph.add((file_resource, SPDX_NAMESPACE.attributionText, Literal(attribution_text)))
