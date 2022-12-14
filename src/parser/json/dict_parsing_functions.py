from datetime import datetime
from typing import Any, Callable, Dict

from src.model.external_document_ref import ExternalDocumentRef
from src.model.typing.constructor_type_errors import ConstructorTypeErrors
from src.parser.error import SPDXParsingError


def parse_optional_field(field: Any, method_to_parse:Callable=lambda x: x, default=None):
    if not field:
        return default
    return method_to_parse(field)


def datetime_from_str(created: str) -> datetime:
    date = datetime.strptime(created, "%Y-%m-%dT%H:%M:%SZ")
    return date


def transform_json_str_to_enum_name(json_str: str) -> str:
    return json_str.replace("-","_").upper()


def try_construction_raise_parsing_error(object_to_construct: Any, args_for_construction: Dict) -> Any:
    try:
        constructed_object = object_to_construct(**args_for_construction)
    except ConstructorTypeErrors as err:
        raise SPDXParsingError([f"Error while constructing {object_to_construct.__name__}: {err.get_messages()}"])
    return constructed_object
