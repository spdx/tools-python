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
from datetime import datetime
from typing import Any, Optional, Dict

from rdflib import Namespace, Graph, Literal
from rdflib.term import Node

from spdx.datetime_conversions import datetime_to_iso_string
from spdx.model.spdx_no_assertion import SpdxNoAssertion
from spdx.model.spdx_none import SpdxNone
from spdx.validation.spdx_id_validators import is_valid_internal_spdx_id

SPDX_NAMESPACE = Namespace("http://spdx.org/rdf/terms#")
POINTER_NAMESPACE = Namespace("http://www.w3.org/2009/pointers#")


def add_literal_value(graph: Graph, parent: Node, predicate: Node, value: Any):
    if value is None:
        return
    if isinstance(value, list):
        for element in value:
            element_triple = (parent, predicate, Literal(str(element)))
            graph.add(element_triple)
    graph.add((parent, predicate, Literal(str(value))))
    return


def add_literal_or_no_assertion_or_none(graph: Graph, parent: Node, predicate: Node, value: Any):
    if value is None:
        return
    if isinstance(value, SpdxNone):
        graph.add((parent, predicate, SPDX_NAMESPACE.none))
        return
    add_literal_or_no_assertion(graph, parent, predicate, value)


def add_literal_or_no_assertion(graph: Graph, parent: Node, predicate: Node, value: Any):
    if value is None:
        return
    if isinstance(value, SpdxNoAssertion):
        graph.add((parent, predicate, SPDX_NAMESPACE.noassertion))
        return
    add_literal_value(graph, parent, predicate, value)


def add_datetime_to_graph(graph: Graph, parent: Node, predicate: Node, value: Optional[datetime]):
    if value:
        graph.add((parent, predicate, Literal(datetime_to_iso_string(value))))


def add_namespace_to_spdx_id(spdx_id: str, doc_namespace: str, external_doc_namespaces: Dict[str, str]) -> str:
    if ":" in spdx_id:
        external_doc_ref_id = spdx_id.split(":")[0]
        return f"{external_doc_namespaces[external_doc_ref_id]}#{spdx_id.split(':')[1]}"

    if is_valid_internal_spdx_id(spdx_id):
        return f"{doc_namespace}#{spdx_id}"

    return spdx_id
