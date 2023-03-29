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
from typing import Union

from rdflib import Graph, RDF
from license_expression import LicenseExpression, get_spdx_licensing
from rdflib.term import Identifier, URIRef, BNode, Node
from spdx.parser.rdf.graph_parsing_functions import remove_prefix

from spdx.rdfschema.namespace import SPDX_NAMESPACE, LICENSE_NAMESPACE


def parse_license_expression(license_expression_node: Union[URIRef, BNode, Node], graph: Graph,
                             doc_namespace: str) -> LicenseExpression:
    spdx_licensing = get_spdx_licensing()
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
        for (_, _, member_node) in graph.triples((license_expression_node, SPDX_NAMESPACE.member, None)):
            members.append(parse_license_expression(member_node, graph, doc_namespace))
        expression = " AND ".join([str(member) for member in members])
    if node_type == SPDX_NAMESPACE.DisjunctiveLicenseSet:
        members = []
        for (_, _, member_node) in graph.triples((license_expression_node, SPDX_NAMESPACE.member, None)):
            members.append(parse_license_expression(member_node, graph, doc_namespace))
        expression = " OR ".join([str(member) for member in members])
    if node_type == SPDX_NAMESPACE.WithExceptionOperator:
        license_expression = parse_license_expression(graph.value(license_expression_node, SPDX_NAMESPACE.member),
                                                      graph, doc_namespace)
        exception = parse_license_exception(graph.value(license_expression_node, SPDX_NAMESPACE.licenseException),
                                            graph)
        expression = f"{license_expression} WITH {exception}"

    return spdx_licensing.parse(expression)


def parse_license_exception(exception_node: Identifier, graph: Graph) -> str:
    if exception_node.startswith(LICENSE_NAMESPACE):
        exception = remove_prefix(exception_node, LICENSE_NAMESPACE)
    else:
        exception = graph.value(exception_node, SPDX_NAMESPACE.licenseExceptionId).toPython()
    return exception
