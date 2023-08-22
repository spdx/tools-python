# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import os
from unittest import TestCase

from rdflib import RDF, Graph

from spdx_tools.common.spdx_licensing import spdx_licensing
from spdx_tools.spdx.parser.rdf import rdf_parser
from spdx_tools.spdx.parser.rdf.license_expression_parser import parse_license_expression
from spdx_tools.spdx.rdfschema.namespace import SPDX_NAMESPACE


def test_license_expression_parser():
    graph = Graph().parse(os.path.join(os.path.dirname(__file__), "data/file_to_test_rdf_parser.rdf.xml"))
    package_node = graph.value(predicate=RDF.type, object=SPDX_NAMESPACE.Package)
    license_expression_node = graph.value(subject=package_node, predicate=SPDX_NAMESPACE.licenseConcluded)

    license_expression = parse_license_expression(license_expression_node, graph, "https://some.namespace#")

    assert license_expression == spdx_licensing.parse("GPL-2.0 AND MIT")


def test_license_expression_parser_with_coupled_licenses():
    doc = rdf_parser.parse_from_file(
        os.path.join(os.path.dirname(__file__), "../../data/SPDXRdfExample-v2.3.spdx.rdf.xml")
    )

    packages_by_spdx_id = {package.spdx_id: package for package in doc.packages}
    files_by_spdx_id = {file.spdx_id: file for file in doc.files}

    assert packages_by_spdx_id["SPDXRef-Package"].license_declared == spdx_licensing.parse(
        "LGPL-2.0-only AND LicenseRef-3"
    )
    assert packages_by_spdx_id["SPDXRef-Package"].license_concluded == spdx_licensing.parse(
        "LGPL-2.0-only OR LicenseRef-3"
    )
    TestCase().assertCountEqual(
        packages_by_spdx_id["SPDXRef-Package"].license_info_from_files,
        [
            spdx_licensing.parse("GPL-2.0"),
            spdx_licensing.parse("LicenseRef-1"),
            spdx_licensing.parse("LicenseRef-2"),
        ],
    )

    assert files_by_spdx_id["SPDXRef-JenaLib"].license_concluded == spdx_licensing.parse("LicenseRef-1")
