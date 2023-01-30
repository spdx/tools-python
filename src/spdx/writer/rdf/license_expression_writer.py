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
from typing import Union, List

from boolean import Expression
from rdflib import Graph, URIRef, BNode, RDF
from license_expression import AND, OR, LicenseWithExceptionSymbol, LicenseSymbol, get_spdx_licensing, ExpressionInfo, \
    LicenseExpression
from rdflib.term import Node, Literal

from spdx.model.spdx_no_assertion import SpdxNoAssertion
from spdx.model.spdx_none import SpdxNone

from spdx.writer.rdf.writer_utils import spdx_namespace


def add_license_expression_to_graph(graph: Graph, license_expression: Expression, parent_resource: Node,
                                    doc_namespace: str, predicate: Node):
    if isinstance(license_expression, AND):
        member_node = BNode()
        graph.add((member_node, RDF.type, spdx_namespace.ConjunctiveLicenseSet))
        graph.add((parent_resource, predicate, member_node))
        for arg in license_expression.args:
            add_license_expression_to_graph(graph, arg, member_node, doc_namespace, spdx_namespace.member)
    if isinstance(license_expression, OR):
        member_node = BNode()
        graph.add((member_node, RDF.type, spdx_namespace.DisjunctiveLicenseSet))
        graph.add((parent_resource, predicate, member_node))
        for arg in license_expression.args:
            add_license_expression_to_graph(graph, arg, member_node, doc_namespace, spdx_namespace.member)
    if isinstance(license_expression, LicenseWithExceptionSymbol):
        member_node = BNode()
        graph.add((member_node, RDF.type, spdx_namespace.WithExceptionOperator))
        graph.add((parent_resource, predicate, member_node))

        add_license_expression_to_graph(graph, license_expression.license_symbol, member_node, doc_namespace,
                                        spdx_namespace.member)
        add_license_exception_to_graph(graph, license_expression.exception_symbol, member_node)

    if isinstance(license_expression, LicenseSymbol):
        if check_if_license_or_exception_is_on_spdx_licensing_list(license_expression):
            graph.add(
                (parent_resource, predicate, URIRef(f"http://spdx.org/licenses/{license_expression}")))
        else:
            # assuming that the license expression is a LicenseRef to an instance of ExtractedLicensingInfo
            graph.add((parent_resource, predicate, URIRef(f"{doc_namespace}#{license_expression}")))


def add_license_exception_to_graph(graph: Graph, license_exception: LicenseSymbol, member_node: Node):
    if check_if_license_or_exception_is_on_spdx_licensing_list(license_exception):
        exception_node = URIRef(f"http://spdx.org/licenses/{license_exception}")
        graph.add((member_node, spdx_namespace.licenseException, exception_node))
    else:
        exception_node = BNode()
        graph.add((exception_node, spdx_namespace.licenseExceptionId, Literal(license_exception)))
        graph.add((member_node, spdx_namespace.licenseException, exception_node))

    graph.add((exception_node, RDF.type, spdx_namespace.LicenseException))


def check_if_license_or_exception_is_on_spdx_licensing_list(license_symbol: LicenseSymbol) -> bool:
    symbol_info: ExpressionInfo = get_spdx_licensing().validate(license_symbol)
    return not symbol_info.errors


def add_license_expression_or_none_or_no_assertion(graph: Graph, parent: Node, predicate: Node, value: Union[
    List[LicenseExpression], LicenseExpression, SpdxNoAssertion, SpdxNone], doc_namespace: str):
    if isinstance(value, SpdxNoAssertion):
        graph.add((parent, predicate, spdx_namespace.noassertion))
        return
    if isinstance(value, SpdxNone):
        graph.add((parent, predicate, spdx_namespace.none))
        return
    if isinstance(value, list):
        for license_expression in value:
            add_license_expression_to_graph(graph, license_expression, parent, doc_namespace, predicate)
    if isinstance(value, LicenseExpression):
        add_license_expression_to_graph(graph, value, parent, doc_namespace, predicate)
