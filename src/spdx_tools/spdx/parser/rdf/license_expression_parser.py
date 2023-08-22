# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from beartype.typing import Optional, Union
from license_expression import LicenseExpression
from rdflib import RDF, Graph
from rdflib.term import BNode, Identifier, Node, URIRef

from spdx_tools.common.spdx_licensing import spdx_licensing
from spdx_tools.spdx.parser.logger import Logger
from spdx_tools.spdx.parser.rdf.graph_parsing_functions import get_value_from_graph, remove_prefix
from spdx_tools.spdx.rdfschema.namespace import LICENSE_NAMESPACE, SPDX_NAMESPACE


def parse_license_expression(
    license_expression_node: Union[URIRef, BNode, Node],
    graph: Graph,
    doc_namespace: str,
    logger: Optional[Logger] = None,
) -> LicenseExpression:
    if not logger:
        logger = Logger()

    expression = ""
    if license_expression_node.startswith(LICENSE_NAMESPACE):
        expression = remove_prefix(license_expression_node, LICENSE_NAMESPACE)
        return spdx_licensing.parse(expression)
    if license_expression_node.startswith(doc_namespace):
        expression = license_expression_node.fragment
        return spdx_licensing.parse(expression)

    node_type = graph.value(license_expression_node, RDF.type)
    if node_type == SPDX_NAMESPACE.ConjunctiveLicenseSet:
        members = []
        for _, _, member_node in graph.triples((license_expression_node, SPDX_NAMESPACE.member, None)):
            members.append(parse_license_expression(member_node, graph, doc_namespace, logger))
        expression = " AND ".join([str(member) for member in members])
    if node_type == SPDX_NAMESPACE.DisjunctiveLicenseSet:
        members = []
        for _, _, member_node in graph.triples((license_expression_node, SPDX_NAMESPACE.member, None)):
            members.append(parse_license_expression(member_node, graph, doc_namespace, logger))
        expression = " OR ".join([str(member) for member in members])
    if node_type == SPDX_NAMESPACE.WithExceptionOperator:
        license_expression = parse_license_expression(
            graph.value(license_expression_node, SPDX_NAMESPACE.member), graph, doc_namespace, logger
        )
        exception = parse_license_exception(
            get_value_from_graph(logger, graph, license_expression_node, SPDX_NAMESPACE.licenseException),
            graph,
            logger,
        )
        expression = f"{license_expression} WITH {exception}"

    return spdx_licensing.parse(expression)


def parse_license_exception(exception_node: Identifier, graph: Graph, logger) -> str:
    if exception_node.startswith(LICENSE_NAMESPACE):
        exception = remove_prefix(exception_node, LICENSE_NAMESPACE)
    else:
        exception = get_value_from_graph(logger, graph, exception_node, SPDX_NAMESPACE.licenseExceptionId).toPython()
    return exception
