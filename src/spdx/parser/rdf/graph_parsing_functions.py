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
from typing import Any, Callable, Union, Optional

from rdflib import Graph, URIRef
from rdflib.exceptions import UniquenessError
from rdflib.term import Node

from spdx.model.spdx_no_assertion import SpdxNoAssertion, SPDX_NO_ASSERTION_STRING
from spdx.model.spdx_none import SpdxNone, SPDX_NONE_STRING
from spdx.parser.logger import Logger
from spdx.rdfschema.namespace import SPDX_NAMESPACE


def parse_literal(logger: Logger, graph: Graph, subject: Node, predicate: Node, default: Any = None,
                  method_to_apply: Callable = lambda x: x, prefix: str = ""):
    try:
        value = graph.value(subject=subject, predicate=predicate, default=default, any=False)
    except UniquenessError:
        logger.append(f"Multiple values for unique value {predicate} found.")
        return

    if value:
        return method_to_apply(value.removeprefix(prefix))

    return default


def parse_literal_or_no_assertion_or_none(logger: Logger, graph: Graph, subject: Node, predicate: Node,
                                          default: Any = None, method_to_apply: Callable = lambda x: x):
    try:
        value = graph.value(subject=subject, predicate=predicate, default=default, any=False)
    except UniquenessError:
        logger.append(f"Multiple values for unique value {predicate} found.")
        return
    if not value:
        return default
    if value == SPDX_NAMESPACE.noassertion:
        return SpdxNoAssertion()
    if value == SPDX_NAMESPACE.none:
        return SpdxNone()
    return method_to_apply(value.toPython())


def str_to_no_assertion_or_none(value: str) -> Union[str, SpdxNone, SpdxNoAssertion]:
    if value == SPDX_NO_ASSERTION_STRING:
        return SpdxNoAssertion()
    if value == SPDX_NONE_STRING:
        return SpdxNone()
    return value


def parse_spdx_id(resource: URIRef, doc_namespace: str) -> Optional[str]:
    if not resource:
        return None
    if resource.startswith(f"{doc_namespace}#"):
        spdx_id = resource.fragment
    else:
        spdx_id = resource.toPython()
    return spdx_id or None
