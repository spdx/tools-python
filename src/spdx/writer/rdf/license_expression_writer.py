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

from spdx.rdfschema.namespace import SPDX_NAMESPACE, LICENSE_NAMESPACE


def add_license_expression_or_none_or_no_assertion(value: Union[
    List[Union[LicenseExpression, SpdxNoAssertion, SpdxNone]], LicenseExpression, SpdxNoAssertion, SpdxNone], graph: Graph, parent: Node, predicate: Node,
                                                   doc_namespace: str):
    if isinstance(value, SpdxNoAssertion):
        graph.add((parent, predicate, SPDX_NAMESPACE.noassertion))
        return
    if isinstance(value, SpdxNone):
        graph.add((parent, predicate, SPDX_NAMESPACE.none))
        return
    if isinstance(value, list):
        for license_expression in value:
            add_license_expression_or_none_or_no_assertion(license_expression, graph, parent, predicate, doc_namespace)
    if isinstance(value, LicenseExpression):
        add_license_expression_to_graph(value, graph, parent, predicate, doc_namespace)


def add_license_expression_to_graph(license_expression: Expression, graph: Graph, parent: Node, predicate: Node,
                                    doc_namespace: str):
    if isinstance(license_expression, AND):
        member_node = BNode()
        graph.add((member_node, RDF.type, SPDX_NAMESPACE.ConjunctiveLicenseSet))
        graph.add((parent, predicate, member_node))
        for arg in license_expression.args:
            add_license_expression_to_graph(arg, graph, member_node, SPDX_NAMESPACE.member, doc_namespace)
    if isinstance(license_expression, OR):
        member_node = BNode()
        graph.add((member_node, RDF.type, SPDX_NAMESPACE.DisjunctiveLicenseSet))
        graph.add((parent, predicate, member_node))
        for arg in license_expression.args:
            add_license_expression_to_graph(arg, graph, member_node, SPDX_NAMESPACE.member, doc_namespace)
    if isinstance(license_expression, LicenseWithExceptionSymbol):
        member_node = BNode()
        graph.add((member_node, RDF.type, SPDX_NAMESPACE.WithExceptionOperator))
        graph.add((parent, predicate, member_node))

        add_license_expression_to_graph(license_expression.license_symbol, graph, member_node, SPDX_NAMESPACE.member,
                                        doc_namespace)
        add_license_exception_to_graph(license_expression.exception_symbol, graph, member_node)

    if isinstance(license_expression, LicenseSymbol):
        if license_or_exception_is_on_spdx_licensing_list(license_expression):
            graph.add(
                (parent, predicate, LICENSE_NAMESPACE[str(license_expression)]))
        else:
            # assuming that the license expression is a LicenseRef to an instance of ExtractedLicensingInfo
            graph.add((parent, predicate, URIRef(f"{doc_namespace}#{license_expression}")))


def license_or_exception_is_on_spdx_licensing_list(license_symbol: LicenseSymbol) -> bool:
    symbol_info: ExpressionInfo = get_spdx_licensing().validate(license_symbol)
    return not symbol_info.errors


def add_license_exception_to_graph(license_exception: LicenseSymbol, graph: Graph, parent: Node):
    if license_or_exception_is_on_spdx_licensing_list(license_exception):
        exception_node = LICENSE_NAMESPACE[str(license_exception)]
        graph.add((parent, SPDX_NAMESPACE.licenseException, exception_node))
    else:
        exception_node = BNode()
        graph.add((exception_node, SPDX_NAMESPACE.licenseExceptionId, Literal(license_exception)))
        graph.add((parent, SPDX_NAMESPACE.licenseException, exception_node))

    graph.add((exception_node, RDF.type, SPDX_NAMESPACE.LicenseException))
