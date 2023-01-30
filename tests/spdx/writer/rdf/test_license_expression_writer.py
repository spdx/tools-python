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
import pytest
from license_expression import get_spdx_licensing
from rdflib import Graph, URIRef, RDF, Literal
from spdx.writer.rdf.writer_utils import spdx_namespace

from spdx.writer.rdf.license_expression_writer import add_license_expression_to_graph


def test_add_conjunctive_license_set_to_graph():
    graph = Graph()
    license_expression = get_spdx_licensing().parse("MIT AND GPL-2.0")

    add_license_expression_to_graph(graph, URIRef("anyURI"), spdx_namespace.licenseConcluded, license_expression,
                                    "https://namespace")

    assert (None, RDF.type, spdx_namespace.ConjunctiveLicenseSet) in graph
    assert (None, spdx_namespace.member, URIRef("http://spdx.org/licenses/MIT")) in graph
    assert (None, spdx_namespace.member, URIRef("http://spdx.org/licenses/GPL-2.0-only")) in graph


def test_add_disjunctive_license_set_to_graph():
    graph = Graph()
    license_expression = get_spdx_licensing().parse("MIT OR GPL-2.0")

    add_license_expression_to_graph(graph, URIRef("anyURI"), spdx_namespace.licenseConcluded, license_expression,
                                    "https://namespace")

    assert (None, RDF.type, spdx_namespace.DisjunctiveLicenseSet) in graph
    assert (None, spdx_namespace.member, URIRef("http://spdx.org/licenses/MIT")) in graph
    assert (None, spdx_namespace.member, URIRef("http://spdx.org/licenses/GPL-2.0-only")) in graph


@pytest.mark.parametrize("license_with_exception,expected_triple", [("MIT WITH openvpn-openssl-exception", (
    URIRef("http://spdx.org/licenses/openvpn-openssl-exception"), RDF.type, spdx_namespace.LicenseException)),
                                                                    ("MIT WITH unknown-exception", (
                                                                        None,
                                                                        spdx_namespace.licenseExceptionId,
                                                                        Literal("unknown-exception")))])
def test_license_exception_to_graph(license_with_exception, expected_triple):
    graph = Graph()
    license_expression = get_spdx_licensing().parse(license_with_exception)

    add_license_expression_to_graph(graph, URIRef("anyURI"), spdx_namespace.licenseConcluded, license_expression,
                                    "https://namespace")

    assert (None, RDF.type, spdx_namespace.WithExceptionOperator) in graph
    assert (None, spdx_namespace.member, URIRef("http://spdx.org/licenses/MIT")) in graph
    assert (None, spdx_namespace.licenseException, None) in graph
    assert expected_triple in graph
