# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import logging
from datetime import datetime

from beartype.typing import Any, Dict, Optional
from rdflib import Graph, Literal
from rdflib.term import Node

from spdx_tools.spdx.datetime_conversions import datetime_to_iso_string
from spdx_tools.spdx.model import SpdxNoAssertion, SpdxNone
from spdx_tools.spdx.rdfschema.namespace import SPDX_NAMESPACE
from spdx_tools.spdx.validation.spdx_id_validators import is_valid_internal_spdx_id


def add_optional_literal(value: Any, graph: Graph, parent: Node, predicate: Node):
    if value is None:
        return
    if isinstance(value, list):
        for element in value:
            graph.add((parent, predicate, Literal(str(element))))
        return
    graph.add((parent, predicate, Literal(str(value))))


def add_literal_or_no_assertion_or_none(value: Any, graph: Graph, parent: Node, predicate: Node):
    if value is None:
        return
    if isinstance(value, SpdxNone):
        graph.add((parent, predicate, SPDX_NAMESPACE.none))
        return
    add_literal_or_no_assertion(value, graph, parent, predicate)


def add_literal_or_no_assertion(value: Any, graph: Graph, parent: Node, predicate: Node):
    if value is None:
        return
    if isinstance(value, SpdxNoAssertion):
        graph.add((parent, predicate, SPDX_NAMESPACE.noassertion))
        return
    add_optional_literal(value, graph, parent, predicate)


def add_datetime_to_graph(value: Optional[datetime], graph: Graph, parent: Node, predicate: Node):
    if value:
        graph.add((parent, predicate, Literal(datetime_to_iso_string(value))))


def add_namespace_to_spdx_id(spdx_id: str, doc_namespace: str, external_doc_namespaces: Dict[str, str]) -> str:
    if ":" in spdx_id:
        external_doc_ref_id = spdx_id.split(":")[0]
        if external_doc_ref_id not in external_doc_namespaces.keys():
            logging.warning(f"No namespace for external document reference with id {external_doc_ref_id} provided.")
            return spdx_id
        return f"{external_doc_namespaces[external_doc_ref_id]}#{spdx_id.split(':')[1]}"

    if is_valid_internal_spdx_id(spdx_id):
        return f"{doc_namespace}#{spdx_id}"

    return spdx_id
