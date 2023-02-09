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

from license_expression import get_spdx_licensing
from rdflib import Graph, RDF, URIRef

from spdx.parser.rdf.license_expression_parser import parse_license_expression
from spdx.rdfschema.namespace import SPDX_NAMESPACE
from spdx.writer.rdf.license_expression_writer import add_license_expression_to_graph


def test_license_expression_parser():
    graph = Graph().parse(os.path.join(os.path.dirname(__file__), "data/file_to_test_rdf_parser.rdf.xml"))
    package_node = graph.value(predicate=RDF.type, object=SPDX_NAMESPACE.Package)
    license_expression_node = graph.value(subject=package_node, predicate=SPDX_NAMESPACE.licenseConcluded)

    license_expression = parse_license_expression(license_expression_node, graph)

    assert license_expression == get_spdx_licensing().parse("GPL-2.0 AND MIT")

def test_license_expression_parser_with_writer():
    license_expression = get_spdx_licensing().parse("GPL-2.0 WITH exception")
    graph = Graph()
    add_license_expression_to_graph(license_expression, graph, URIRef("test"), URIRef("predicate"), "anyURI")

    expression_noe = graph.value(URIRef("test"), URIRef("predicate"))
    license_expression_parsed = parse_license_expression(expression_noe,graph)

    assert license_expression_parsed == license_expression
