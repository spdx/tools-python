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
import os

from rdflib import Graph, RDF

from spdx.parser.rdf.snippet_parser import parse_snippet
from spdx.rdfschema.namespace import SPDX_NAMESPACE


def test_parse_snippet():
    graph = Graph().parse(os.path.join(os.path.dirname(__file__), "data/file_to_test_rdf_parser.rdf.xml"))
    snippet_node = graph.value(predicate=RDF.type, object=SPDX_NAMESPACE.Snippet)
    doc_namespace = "https://some.namespace"

    snippet = parse_snippet(snippet_node, graph, doc_namespace)

    assert snippet.spdx_id == "SPDXRef-Snippet"
    assert snippet.file_spdx_id == "SPDXRef-File"
    assert snippet.byte_range == (1, 2)
    assert snippet.line_range == (3, 4)
    assert snippet.license_concluded == None
    assert snippet.license_info_in_snippet == None
    assert snippet.license_comment == "snippetLicenseComment"
    assert snippet.copyright_text == "licenseCopyrightText"
    assert snippet.comment == "snippetComment"
    assert snippet.name == "snippetName"
    assert snippet.attribution_texts == ["snippetAttributionText"]
