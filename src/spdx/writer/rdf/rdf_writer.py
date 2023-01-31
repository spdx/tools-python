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
from typing import Dict, List

from rdflib import Graph, DOAP
from rdflib.compare import to_isomorphic

from spdx.model.document import Document
from spdx.validation.document_validator import validate_full_spdx_document
from spdx.validation.validation_message import ValidationMessage
from spdx.writer.rdf.annotation_writer import add_annotation_to_graph
from spdx.writer.rdf.creation_info_writer import add_creation_info_to_graph
from spdx.writer.rdf.extracted_licensing_info_writer import add_extracted_licensing_info_to_graph
from spdx.writer.rdf.file_writer import add_file_to_graph
from spdx.writer.rdf.package_writer import add_package_to_graph
from spdx.writer.rdf.relationship_writer import add_relationship_to_graph
from spdx.writer.rdf.snippet_writer import add_snippet_to_graph
from spdx.rdfschema.namespace import SPDX_NAMESPACE, POINTER_NAMESPACE


def write_document_to_file(document: Document, file_name: str, validate: bool):
    if validate:
        validation_messages: List[ValidationMessage] = validate_full_spdx_document(document,
                                                                                   document.creation_info.spdx_version)
        if validation_messages:
            raise ValueError(f"Document is not valid. The following errors were detected: {validation_messages}")

    graph = Graph()
    doc_namespace = document.creation_info.document_namespace
    external_doc_ref_to_namespace: Dict[str, str] = {external_doc_ref.document_ref_id: external_doc_ref.document_uri for
                                                     external_doc_ref in document.creation_info.external_document_refs}
    doc_node = add_creation_info_to_graph(document.creation_info, graph)
    for annotation in document.annotations:
        add_annotation_to_graph(annotation, graph, doc_namespace, external_doc_ref_to_namespace)

    for file in document.files:
        add_file_to_graph(file, graph, doc_namespace, external_doc_ref_to_namespace)

    for package in document.packages:
        add_package_to_graph(package, graph, doc_namespace, external_doc_ref_to_namespace)

    for relationship in document.relationships:
        add_relationship_to_graph(relationship, graph, doc_namespace, external_doc_ref_to_namespace)

    for snippet in document.snippets:
        add_snippet_to_graph(snippet, graph, doc_namespace, external_doc_ref_to_namespace)

    for extracted_licensing_info in document.extracted_licensing_info:
        add_extracted_licensing_info_to_graph(extracted_licensing_info, graph, doc_node, doc_namespace)

    graph = to_isomorphic(graph)
    graph.bind("spdx", SPDX_NAMESPACE)
    graph.bind("doap", DOAP)
    graph.bind("ptr", POINTER_NAMESPACE)
    graph.serialize(file_name, "pretty-xml", encoding="UTF-8", max_depth=100)
