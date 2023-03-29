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
from spdx.rdfschema.namespace import SPDX_NAMESPACE

from spdx.writer.rdf.license_expression_writer import add_license_expression_to_graph


def test_add_conjunctive_license_set_to_graph():
    graph = Graph()
    license_expression = get_spdx_licensing().parse("MIT AND GPL-2.0")

    add_license_expression_to_graph(license_expression, graph, URIRef("parentNode"), SPDX_NAMESPACE.licenseConcluded,
                                    "https://namespace")

    assert (URIRef("parentNode"), SPDX_NAMESPACE.licenseConcluded, None) in graph
    assert (None, RDF.type, SPDX_NAMESPACE.ConjunctiveLicenseSet) in graph
    assert (None, SPDX_NAMESPACE.member, URIRef("http://spdx.org/licenses/MIT")) in graph
    assert (None, SPDX_NAMESPACE.member, URIRef("http://spdx.org/licenses/GPL-2.0-only")) in graph


def test_add_disjunctive_license_set_to_graph():
    graph = Graph()
    license_expression = get_spdx_licensing().parse("MIT OR GPL-2.0")

    add_license_expression_to_graph(license_expression, graph, URIRef("parentNode"), SPDX_NAMESPACE.licenseConcluded,
                                    "https://namespace")

    assert (URIRef("parentNode"), SPDX_NAMESPACE.licenseConcluded, None) in graph
    assert (None, RDF.type, SPDX_NAMESPACE.DisjunctiveLicenseSet) in graph
    assert (None, SPDX_NAMESPACE.member, URIRef("http://spdx.org/licenses/MIT")) in graph
    assert (None, SPDX_NAMESPACE.member, URIRef("http://spdx.org/licenses/GPL-2.0-only")) in graph


@pytest.mark.parametrize("license_with_exception,"
                         "expected_triple", [("MIT WITH openvpn-openssl-exception",
                                              (URIRef("http://spdx.org/licenses/openvpn-openssl-exception"), RDF.type,
                                               SPDX_NAMESPACE.LicenseException)),
                                             ("MIT WITH unknown-exception",
                                              (None, SPDX_NAMESPACE.licenseExceptionId, Literal("unknown-exception")))])
def test_license_exception_to_graph(license_with_exception, expected_triple):
    graph = Graph()
    license_expression = get_spdx_licensing().parse(license_with_exception)

    add_license_expression_to_graph(license_expression, graph, URIRef("parentNode"), SPDX_NAMESPACE.licenseConcluded,
                                    "https://namespace")

    assert (URIRef("parentNode"), SPDX_NAMESPACE.licenseConcluded, None) in graph
    assert (None, RDF.type, SPDX_NAMESPACE.WithExceptionOperator) in graph
    assert (None, SPDX_NAMESPACE.member, URIRef("http://spdx.org/licenses/MIT")) in graph
    assert (None, SPDX_NAMESPACE.licenseException, None) in graph
    assert expected_triple in graph
