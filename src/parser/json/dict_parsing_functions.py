from datetime import datetime
from typing import Any, Callable, Dict

from src.model.typing.constructor_type_errors import ConstructorTypeErrors
from src.parser.error import SPDXParsingError
from src.parser.logger import Logger


def parse_optional_field(field: Any, method_to_parse: Callable = lambda x: x, default=None):
    if not field:
        return default
    return method_to_parse(field)


def datetime_from_str(date_str: str) -> datetime:
    if not isinstance(date_str, str):
        raise SPDXParsingError([f"Could not convert str to datetime, invalid type: {type(date_str).__name__}"])
    date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
    return date


def transform_json_str_to_enum_name(json_str: str) -> str:
    return json_str.replace("-", "_").upper()


def try_construction_raise_parsing_error(object_to_construct: Any, args_for_construction: Dict) -> Any:
    try:
        constructed_object = object_to_construct(**args_for_construction)
    except ConstructorTypeErrors as err:
        raise SPDXParsingError([f"Error while constructing {object_to_construct.__name__}: {err.get_messages()}"])
    return constructed_object


def try_parse_optional_field_append_logger_when_failing(logger: Logger, field: Any, method_to_parse: Callable, default=None):
    try:
        parsed_element = parse_optional_field(field=field, method_to_parse=method_to_parse, default=default)
    except SPDXParsingError as err:
        logger.append_all(err.get_messages())
        parsed_element = default
    return parsed_element

def try_parse_required_field_append_logger_when_failing(logger: Logger, field: Any, method_to_parse: Callable, default=None):
    try:
        parsed_element = method_to_parse(field)
    except SPDXParsingError as err:
        logger.append_all(err.get_messages())
        parsed_element = default
    return parsed_element

