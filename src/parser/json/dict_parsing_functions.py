from datetime import datetime
from typing import Dict, Any, List, Union, Optional, Callable

from src.model.license_expression import LicenseExpression
from src.model.spdx_no_assertion import SpdxNoAssertion
from src.model.spdx_none import SpdxNone

from src.parser.logger import Logger

def parse_optional_field(field: Any, method_to_parse:Callable=lambda x: x, default=None):
    if not field:
        return default
    return method_to_parse(field)


def datetime_from_str(created: str) -> datetime:
    date = datetime.strptime(created, "%Y-%m-%dT%H:%M:%SZ")
    return date

def parse_license_expression(license_expression: Union[str, List[str]]) -> Union[LicenseExpression, SpdxNoAssertion, SpdxNone, List[LicenseExpression]]:
    if license_expression == SpdxNone.__str__:
        return SpdxNone()
    if license_expression == SpdxNoAssertion.__str__:
        return SpdxNoAssertion()
    elif isinstance(license_expression, str):
        return LicenseExpression(license_expression)
    elif isinstance(license_expression, list):
        return list(map(parse_license_expression, license_expression))

def transform_json_str_to_enum_name(json_str: str) -> str:
    return json_str.replace("-","_").upper()
