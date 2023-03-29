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
from typing import Any, Dict

from common.typing.constructor_type_errors import ConstructorTypeErrors
from spdx.parser.error import SPDXParsingError
from spdx.parser.logger import Logger


def construct_or_raise_parsing_error(object_to_construct: Any, args_for_construction: Dict) -> Any:
    try:
        constructed_object = object_to_construct(**args_for_construction)
    except ConstructorTypeErrors as err:
        raise SPDXParsingError([f"Error while constructing {object_to_construct.__name__}: {err.get_messages()}"])
    except TypeError as err:
        raise SPDXParsingError([f"Error while constructing {object_to_construct.__name__}: {err.args[0]}"])
    return constructed_object


def raise_parsing_error_if_logger_has_messages(logger: Logger, parsed_object_name: str = None):
    if logger.has_messages():
        if parsed_object_name:
            raise SPDXParsingError([f"Error while parsing {parsed_object_name}: {logger.get_messages()}"])
        else:
            raise SPDXParsingError(logger.get_messages())
