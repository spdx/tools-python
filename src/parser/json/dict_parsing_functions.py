# Copyright (c) 2022 spdx contributors
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
from typing import Any, Callable, Dict, List

from src.model.typing.constructor_type_errors import ConstructorTypeErrors
from src.parser.error import SPDXParsingError
from src.parser.logger import Logger


def datetime_from_str(date_str: str) -> datetime:
    if not isinstance(date_str, str):
        raise SPDXParsingError([f"Could not convert str to datetime, invalid type: {type(date_str).__name__}"])
    try:
        date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        raise SPDXParsingError(
            [f'Could not convert str to datetime, format of {date_str} does not match "%Y-%m-%dT%H:%M:%SZ"'])
    return date


def json_str_to_enum_name(json_str: str) -> str:
    return json_str.replace("-", "_").upper()


def construct_or_raise_parsing_error(object_to_construct: Any, args_for_construction: Dict) -> Any:
    try:
        constructed_object = object_to_construct(**args_for_construction)
    except ConstructorTypeErrors as err:
        raise SPDXParsingError([f"Error while constructing {object_to_construct.__name__}: {err.get_messages()}"])
    return constructed_object


def parse_field_or_log_error(logger: Logger, field: Any, parsing_method: Callable = lambda x: x, optional=False,
                             default=None, ) -> Any:
    try:
        if optional:
            if not field:
                return default
            parsed_element = parsing_method(field)
        else:
            parsed_element = parsing_method(field)
    except SPDXParsingError as err:
        logger.extend(err.get_messages())
        parsed_element = default
    return parsed_element


def append_parsed_field_or_log_error(logger: Logger, list_to_append_to: List[Any], field: Any,
                                     method_to_parse: Callable) -> List[Any]:
    try:
        parsed_element = method_to_parse(field)
        list_to_append_to.append(parsed_element)
    except SPDXParsingError as err:
        logger.extend(err.get_messages())
    return list_to_append_to


def raise_parsing_error_if_logger_has_messages(logger: Logger, parsed_object_name: str = None):
    if logger.has_messages():
        if parsed_object_name:
            raise SPDXParsingError([f"Error while parsing {parsed_object_name}: {logger.get_messages()}"])
        else:
            raise SPDXParsingError(logger.get_messages())
