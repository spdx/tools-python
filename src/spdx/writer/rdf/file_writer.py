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

from rdflib import Graph, URIRef, Literal, RDF, RDFS

from spdx.model.file import File
from spdx.writer.rdf.checksum_writer import add_checksum_information_to_graph
from spdx.writer.rdf.writer_utils import spdx_namespace, add_literal_value_if_exists


def add_file_information_to_graph(file: File, graph: Graph, doc_namespace: str):
    file_resource = URIRef(f"{doc_namespace}#{file.spdx_id}")
    graph.add((file_resource, RDF.type, spdx_namespace.File))
    graph.add((file_resource, spdx_namespace.fileName, Literal(file.name)))
    for file_type in file.file_type:
        graph.add((file_resource, spdx_namespace.fileType, spdx_namespace[f"fileType_{file_type.name.lower()}"]))

    for checksum in file.checksums:
        add_checksum_information_to_graph(checksum, graph, file_resource)

    # as long as we don't have a proper handling of the licenses we simply write literals here
    add_literal_value_if_exists(graph, file_resource, spdx_namespace.licenseConcluded, file.license_concluded)
    add_literal_value_if_exists(graph, file_resource, spdx_namespace.licenseInfoInFile, file.license_info_in_file)

    add_literal_value_if_exists(graph, file_resource, spdx_namespace.licenseComments, file.license_comment)
    add_literal_value_if_exists(graph, file_resource, spdx_namespace.copyrightText, file.copyright_text)
    add_literal_value_if_exists(graph, file_resource, RDFS.comment, file.comment)
    add_literal_value_if_exists(graph, file_resource, spdx_namespace.noticeText, file.notice)
    for contributor in file.contributors:
        graph.add((file_resource, spdx_namespace.fileContributor, Literal(contributor)))
    for attribution_text in file.attribution_texts:
        graph.add((file_resource, spdx_namespace.attributionText, Literal(attribution_text)))


