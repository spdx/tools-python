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
from typing import Tuple, Optional, Dict

from rdflib import Graph, URIRef, RDF, RDFS, Literal
from spdx.writer.rdf.writer_utils import spdx_namespace, add_literal_or_no_assertion_or_none, add_literal_value, \
    add_namespace_to_spdx_id

from spdx.model.snippet import Snippet


def add_snippet_information_to_graph(snippet: Snippet, graph: Graph, doc_namespace: str,
                                     external_doc_ref_to_namespace: Dict[str, str]):
    snippet_resource = URIRef(add_namespace_to_spdx_id(snippet.spdx_id, doc_namespace, external_doc_ref_to_namespace))
    graph.add((snippet_resource, RDF.type, spdx_namespace.Snippet))

    graph.add((snippet_resource, spdx_namespace.snippetFromFile,
               URIRef(add_namespace_to_spdx_id(snippet.file_spdx_id, doc_namespace, external_doc_ref_to_namespace))))
    add_range_to_graph(graph, snippet_resource, snippet.byte_range, snippet.file_spdx_id)
    add_range_to_graph(graph, snippet_resource, snippet.line_range, snippet.file_spdx_id)
    add_literal_or_no_assertion_or_none(graph, snippet_resource, spdx_namespace.licenseConcluded,
                                        snippet.license_concluded)
    add_literal_or_no_assertion_or_none(graph, snippet_resource, spdx_namespace.licenseInfoInSnippet,
                                        snippet.license_info_in_snippet)
    add_literal_value(graph, snippet_resource, spdx_namespace.licenseComments, snippet.license_comment)
    add_literal_value(graph, snippet_resource, spdx_namespace.copyrightText, snippet.copyright_text)
    add_literal_value(graph, snippet_resource, RDFS.comment, snippet.comment)
    add_literal_value(graph, snippet_resource, spdx_namespace.name, snippet.name)
    for attribution_text in snippet.attribution_texts:
        graph.add((snippet_resource, spdx_namespace.attributionText, Literal(attribution_text)))


def add_range_to_graph(graph: Graph, snippet_resource: URIRef, range_information: Optional[Tuple[int, int]],
                       file_spdx_id: str):
    # TODO: implement writer for ranges (https://github.com/spdx/tools-python/issues/274)
    pass
