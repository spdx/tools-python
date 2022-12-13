from datetime import datetime
from typing import Any, Callable


def parse_optional_field(field: Any, method_to_parse:Callable=lambda x: x, default=None):
    if not field:
        return default
    return method_to_parse(field)


def datetime_from_str(created: str) -> datetime:
    date = datetime.strptime(created, "%Y-%m-%dT%H:%M:%SZ")
    return date


def transform_json_str_to_enum_name(json_str: str) -> str:
    return json_str.replace("-","_").upper()
