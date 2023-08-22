# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import pytest
from rdflib import RDF, Graph, Literal, URIRef

from spdx_tools.common.spdx_licensing import spdx_licensing
from spdx_tools.spdx.rdfschema.namespace import SPDX_NAMESPACE
from spdx_tools.spdx.writer.rdf.license_expression_writer import add_license_expression_to_graph


def test_add_conjunctive_license_set_to_graph():
    graph = Graph()
    license_expression = spdx_licensing.parse("MIT AND GPL-2.0")

    add_license_expression_to_graph(
        license_expression, graph, URIRef("parentNode"), SPDX_NAMESPACE.licenseConcluded, "https://namespace"
    )

    assert (URIRef("parentNode"), SPDX_NAMESPACE.licenseConcluded, None) in graph
    assert (None, RDF.type, SPDX_NAMESPACE.ConjunctiveLicenseSet) in graph
    assert (None, SPDX_NAMESPACE.member, URIRef("http://spdx.org/licenses/MIT")) in graph
    assert (None, SPDX_NAMESPACE.member, URIRef("http://spdx.org/licenses/GPL-2.0-only")) in graph


def test_add_disjunctive_license_set_to_graph():
    graph = Graph()
    license_expression = spdx_licensing.parse("MIT OR GPL-2.0")

    add_license_expression_to_graph(
        license_expression, graph, URIRef("parentNode"), SPDX_NAMESPACE.licenseConcluded, "https://namespace"
    )

    assert (URIRef("parentNode"), SPDX_NAMESPACE.licenseConcluded, None) in graph
    assert (None, RDF.type, SPDX_NAMESPACE.DisjunctiveLicenseSet) in graph
    assert (None, SPDX_NAMESPACE.member, URIRef("http://spdx.org/licenses/MIT")) in graph
    assert (None, SPDX_NAMESPACE.member, URIRef("http://spdx.org/licenses/GPL-2.0-only")) in graph


@pytest.mark.parametrize(
    "license_with_exception," "expected_triple",
    [
        (
            "MIT WITH openvpn-openssl-exception",
            (URIRef("http://spdx.org/licenses/openvpn-openssl-exception"), RDF.type, SPDX_NAMESPACE.LicenseException),
        ),
        ("MIT WITH unknown-exception", (None, SPDX_NAMESPACE.licenseExceptionId, Literal("unknown-exception"))),
    ],
)
def test_license_exception_to_graph(license_with_exception, expected_triple):
    graph = Graph()
    license_expression = spdx_licensing.parse(license_with_exception)

    add_license_expression_to_graph(
        license_expression, graph, URIRef("parentNode"), SPDX_NAMESPACE.licenseConcluded, "https://namespace"
    )

    assert (URIRef("parentNode"), SPDX_NAMESPACE.licenseConcluded, None) in graph
    assert (None, RDF.type, SPDX_NAMESPACE.WithExceptionOperator) in graph
    assert (None, SPDX_NAMESPACE.member, URIRef("http://spdx.org/licenses/MIT")) in graph
    assert (None, SPDX_NAMESPACE.licenseException, None) in graph
    assert expected_triple in graph
