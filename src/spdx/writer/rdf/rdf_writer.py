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
from rdflib import Graph, Namespace, URIRef, RDF

from spdx.model.document import Document


def write_document_to_file(document: Document, file_name: str):
    spdx_namespace = Namespace("http://spdx.org/rdf/terms#")
    doc_node = URIRef("http://www.spdx.org/tools#SPDXRef-DOCUMENT")
    graph = Graph()
    graph.bind("spdx", spdx_namespace)
    graph.add((doc_node, RDF.type, spdx_namespace.SpdxDocument))


    graph.serialize(file_name, "pretty-xml", encoding="UTF-8")
