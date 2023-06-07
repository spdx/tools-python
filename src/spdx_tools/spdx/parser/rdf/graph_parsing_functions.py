# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from enum import Enum

from beartype.typing import Any, Callable, Optional, Tuple, Type, Union
from rdflib import RDF, Graph, URIRef
from rdflib.exceptions import UniquenessError
from rdflib.namespace import NamespaceManager
from rdflib.term import BNode, Literal, Node

from spdx_tools.spdx.casing_tools import camel_case_to_snake_case
from spdx_tools.spdx.model import SpdxNoAssertion, SpdxNone
from spdx_tools.spdx.model.spdx_no_assertion import SPDX_NO_ASSERTION_STRING
from spdx_tools.spdx.model.spdx_none import SPDX_NONE_STRING
from spdx_tools.spdx.parser.error import SPDXParsingError
from spdx_tools.spdx.parser.logger import Logger
from spdx_tools.spdx.rdfschema.namespace import SPDX_NAMESPACE


def parse_literal(
    logger: Logger,
    graph: Graph,
    subject: Node,
    predicate: Node,
    parsing_method: Callable = lambda x: x.strip(),
    default: Any = None,
):
    value = get_unique_value(logger, graph, subject, predicate, default)
    if not value:
        return default
    return apply_parsing_method_or_log_error(logger, value, parsing_method, default)


def apply_parsing_method_or_log_error(
    logger: Logger, value: Any, parsing_method: Callable = lambda x: x.strip(), default: Any = None
):
    try:
        return parsing_method(value)
    except SPDXParsingError as err:
        logger.extend(err.get_messages())
    except (TypeError, ValueError) as err:
        logger.append(err.args[0])
    return default


def parse_literal_or_no_assertion_or_none(
    logger: Logger,
    graph: Graph,
    subject: Node,
    predicate: Node,
    parsing_method: Callable = lambda x: x.strip(),
    default: Any = None,
):
    value = get_unique_value(logger, graph, subject, predicate, default)
    return get_correctly_typed_value(logger, value, parsing_method, default)


def get_correctly_typed_value(
    logger: Logger, value: Any, parsing_method: Callable = lambda x: x.strip(), default: Any = None
):
    if not value:
        return default
    if value == SPDX_NAMESPACE.noassertion or value.toPython() == SPDX_NO_ASSERTION_STRING:
        return SpdxNoAssertion()
    if value == SPDX_NAMESPACE.none or value.toPython() == SPDX_NONE_STRING:
        return SpdxNone()
    return apply_parsing_method_or_log_error(logger, value, parsing_method, default)


def get_unique_value(logger: Logger, graph: Graph, subject: Node, predicate: Node, default: Any) -> Any:
    try:
        value = graph.value(subject=subject, predicate=predicate, default=default, any=False)
        return value
    except UniquenessError:
        logger.append(f"Multiple values for unique value {predicate} found.")
        return default


def parse_enum_value(enum_str: str, enum_class: Type[Enum], prefix: str) -> Enum:
    try:
        enum_without_rdf_prefix = remove_prefix(enum_str, prefix)
        value = camel_case_to_snake_case(enum_without_rdf_prefix).upper()
        return enum_class[value]
    except KeyError:
        raise SPDXParsingError([f"Invalid value for {enum_class}: {enum_str}"])


def parse_spdx_id(resource: Union[URIRef, BNode], doc_namespace: str, graph: Graph) -> Optional[str]:
    if not resource or isinstance(resource, BNode):
        return None
    if resource.startswith(f"{doc_namespace}#"):
        return resource.fragment
    if "#" in resource:
        namespace_manager = NamespaceManager(graph)
        return namespace_manager.normalizeUri(resource)
    return resource.toPython() or None


# Python 3.9 introduced the method removeprefix() for strings, but as we are also supporting Python 3.7 and 3.8 we need
# to write our own helper method to delete prefixes.
def remove_prefix(string: str, prefix: str) -> str:
    if string.startswith(prefix):
        return string[len(prefix) :]
    return string


def get_correctly_typed_triples(
    logger: Logger,
    graph: Graph,
    subject: Optional[Node] = None,
    predicate: Optional[Node] = None,
    _object: Optional[Node] = None,
) -> Tuple[Union[BNode, URIRef], Node, Union[BNode, Literal, URIRef]]:
    # this is a helper method to cast some rdf types from graph.triples() to be compatible with the
    # code that follows
    for s, p, o in graph.triples((subject, predicate, _object)):
        if not isinstance(s, (BNode, URIRef)):
            logger.append(
                f"Warning: Subject {s} should be of type BNode or URIRef, but is {type(s).__name__}. "
                f"This might lead to a failure."
            )
        if not isinstance(o, (BNode, Literal, URIRef)):
            logger.append(
                f"Warning: Object {o} should be of type BNode, Literal or URIRef, but is {type(o).__name__}. "
                f"This might lead to a failure."
            )
        yield s, p, o


def get_value_from_graph(
    logger: Logger,
    graph: Graph,
    subject: Optional[Node] = None,
    predicate: Optional[Node] = RDF.value,
    _object: Optional[Node] = None,
    default: Optional[Any] = None,
    _any: Optional[bool] = True,
) -> Optional[Union[URIRef, Literal, BNode]]:
    # this is a helper method to cast some rdf types from graph.value() to be compatible with the
    # code that follows
    value = graph.value(subject=subject, predicate=predicate, object=_object, default=default, any=_any)
    if value != default and value is not None and not isinstance(value, (URIRef, Literal, BNode)):
        logger.append(
            f"Warning: Node {value} should be of type BNode, Literal or URIRef, but is {type(value).__name__}. "
            f"This might lead to a failure."
        )
    return value
