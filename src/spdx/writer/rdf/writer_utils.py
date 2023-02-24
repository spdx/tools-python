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
import logging
from datetime import datetime
from typing import Any, Optional, Dict

from rdflib import Graph, Literal
from rdflib.term import Node

from spdx.datetime_conversions import datetime_to_iso_string
from spdx.model.spdx_no_assertion import SpdxNoAssertion
from spdx.model.spdx_none import SpdxNone
from spdx.rdfschema.namespace import SPDX_NAMESPACE
from spdx.validation.spdx_id_validators import is_valid_internal_spdx_id


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
