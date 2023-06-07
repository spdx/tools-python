# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from beartype.typing import Any, Callable, Dict, List, Optional

from spdx_tools.spdx.model import SpdxNoAssertion, SpdxNone
from spdx_tools.spdx.parser.error import SPDXParsingError
from spdx_tools.spdx.parser.logger import Logger
from spdx_tools.spdx.parser.parsing_functions import raise_parsing_error_if_logger_has_messages


def json_str_to_enum_name(json_str: str) -> str:
    if not isinstance(json_str, str):
        raise SPDXParsingError([f"Type for enum must be str not {type(json_str).__name__}"])
    return json_str.replace("-", "_").upper()


def parse_field_or_log_error(
    logger: Logger,
    field: Any,
    parsing_method: Callable = lambda x: x,
    default: Any = None,
    field_is_list: bool = False,
) -> Any:
    if not field:
        return default
    try:
        if field_is_list:
            return parse_list_of_elements(field, parsing_method)
        else:
            return parsing_method(field)
    except SPDXParsingError as err:
        logger.extend(err.get_messages())
    except (TypeError, ValueError) as err:
        logger.append(err.args[0])
    return default


def append_parsed_field_or_log_error(
    logger: Logger, list_to_append_to: List[Any], field: Any, method_to_parse: Callable
) -> List[Any]:
    try:
        parsed_element = method_to_parse(field)
        list_to_append_to.append(parsed_element)
    except SPDXParsingError as err:
        logger.extend(err.get_messages())
    except (TypeError, ValueError) as err:
        logger.append(err.args[0])
    return list_to_append_to


def parse_field_or_no_assertion_or_none(field: Optional[str], method_for_field: Callable = lambda x: x) -> Any:
    if field == SpdxNoAssertion().__str__():
        return SpdxNoAssertion()
    elif field == SpdxNone().__str__():
        return SpdxNone()
    else:
        return method_for_field(field)


def parse_field_or_no_assertion(field: Optional[str], method_for_field: Callable = lambda x: x) -> Any:
    if field == SpdxNoAssertion().__str__():
        return SpdxNoAssertion()
    else:
        return method_for_field(field)


def parse_list_of_elements(list_of_elements: List[Dict], method_to_parse_element: Callable, logger=None) -> List[Any]:
    if not logger:
        logger = Logger()
    parsed_elements = []
    for element_dict in list_of_elements:
        parsed_elements = append_parsed_field_or_log_error(
            logger, parsed_elements, element_dict, method_to_parse_element
        )
    raise_parsing_error_if_logger_has_messages(logger)
    return parsed_elements


def delete_duplicates_from_list(list_with_potential_duplicates: List[Any]) -> List[Any]:
    list_without_duplicates = list(dict.fromkeys(list_with_potential_duplicates))
    return list_without_duplicates
