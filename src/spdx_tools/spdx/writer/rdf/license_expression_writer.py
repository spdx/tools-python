# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from beartype.typing import List, Union
from boolean import Expression
from license_expression import AND, OR, ExpressionInfo, LicenseExpression, LicenseSymbol, LicenseWithExceptionSymbol
from rdflib import RDF, BNode, Graph, URIRef
from rdflib.term import Literal, Node

from spdx_tools.common.spdx_licensing import spdx_licensing
from spdx_tools.spdx.model import SpdxNoAssertion, SpdxNone
from spdx_tools.spdx.rdfschema.namespace import LICENSE_NAMESPACE, SPDX_NAMESPACE


def add_license_expression_or_none_or_no_assertion(
    value: Union[
        List[Union[LicenseExpression, SpdxNoAssertion, SpdxNone]], LicenseExpression, SpdxNoAssertion, SpdxNone
    ],
    graph: Graph,
    parent: Node,
    predicate: Node,
    doc_namespace: str,
):
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


def add_license_expression_to_graph(
    license_expression: Expression, graph: Graph, parent: Node, predicate: Node, doc_namespace: str
):
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

        add_license_expression_to_graph(
            license_expression.license_symbol, graph, member_node, SPDX_NAMESPACE.member, doc_namespace
        )
        add_license_exception_to_graph(license_expression.exception_symbol, graph, member_node)

    if isinstance(license_expression, LicenseSymbol):
        if license_or_exception_is_on_spdx_licensing_list(license_expression):
            graph.add((parent, predicate, LICENSE_NAMESPACE[str(license_expression)]))
        else:
            # assuming that the license expression is a LicenseRef to an instance of ExtractedLicensingInfo
            graph.add((parent, predicate, URIRef(f"{doc_namespace}#{license_expression}")))


def license_or_exception_is_on_spdx_licensing_list(license_symbol: LicenseSymbol) -> bool:
    symbol_info: ExpressionInfo = spdx_licensing.validate(license_symbol)
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
