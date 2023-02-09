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
from unittest import TestCase

from license_expression import get_spdx_licensing
from rdflib import Graph, RDF
from spdx.parser.rdf import rdf_parser

from spdx.parser.rdf.license_expression_parser import parse_license_expression
from spdx.rdfschema.namespace import SPDX_NAMESPACE

def test_license_expression_parser():
    graph = Graph().parse(os.path.join(os.path.dirname(__file__), "data/file_to_test_rdf_parser.rdf.xml"))
    package_node = graph.value(predicate=RDF.type, object=SPDX_NAMESPACE.Package)
    license_expression_node = graph.value(subject=package_node, predicate=SPDX_NAMESPACE.licenseConcluded)

    license_expression = parse_license_expression(license_expression_node, graph, "https://some.namespace#")

    assert license_expression == get_spdx_licensing().parse("GPL-2.0 AND MIT")


def test_license_expression_parser_with_coupled_licenses():
    doc = rdf_parser.parse_from_file(
        os.path.join(os.path.dirname(__file__), "../../data/formats/SPDXRdfExample-v2.3.spdx.rdf.xml"))

    packages_by_spdx_id = {package.spdx_id: package for package in doc.packages}
    files_by_spdx_id = {file.spdx_id: file for file in doc.files}

    assert packages_by_spdx_id["SPDXRef-Package"].license_declared == get_spdx_licensing().parse(
        "LGPL-2.0-only AND LicenseRef-3")
    assert packages_by_spdx_id["SPDXRef-Package"].license_concluded == get_spdx_licensing().parse(
        "LGPL-2.0-only OR LicenseRef-3")
    TestCase().assertCountEqual(packages_by_spdx_id["SPDXRef-Package"].license_info_from_files,
                                [get_spdx_licensing().parse("GPL-2.0"), get_spdx_licensing().parse("LicenseRef-1"),
                                 get_spdx_licensing().parse("LicenseRef-2")])

    assert files_by_spdx_id["SPDXRef-JenaLib"].license_concluded == get_spdx_licensing().parse("LicenseRef-1")
