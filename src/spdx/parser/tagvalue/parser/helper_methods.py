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
import re
from typing import Optional, Callable, Any, Dict

from spdx.model.checksum import Checksum, ChecksumAlgorithm
from spdx.parser.error import SPDXParsingError
from spdx.parser.logger import Logger
from spdx.parser.parsing_functions import construct_or_raise_parsing_error


def grammar_rule(doc):
    # this is a helper method to use decorators for the parsing methods instead of docstrings
    def decorate(func):
        func.__doc__ = doc
        return func

    return decorate


def str_from_text(text: Optional[str]) -> Optional[str]:
    regex = re.compile("<text>((.|\n)+)</text>", re.UNICODE)
    match = regex.match(text)
    if match:
        return match.group(1)
    elif isinstance(text, str):
        return text
    else:
        return None


def parse_checksum(logger: Logger, checksum_str: str) -> Optional[Checksum]:
    try:
        algorithm, value = checksum_str.split(":")
    except ValueError:
        logger.append(
            f"Couldn't split value for checksum in algorithm and value.")
        return None
    algorithm = ChecksumAlgorithm[algorithm.upper().replace("-", "_")]
    value = value.strip()
    try:
        checksum = construct_or_raise_parsing_error(Checksum, {"algorithm": algorithm, "value": value})
    except SPDXParsingError as err:
        logger.append(err.get_messages())
        checksum = None
    return checksum


def set_value(parsed_value: Any, dict_to_fill: Dict[str, Any], argument_name: Optional[str] = None,
              method_to_apply: Callable = lambda x: x):
    if not argument_name:
        argument_name = str(parsed_value.slice[0])
    if argument_name in dict_to_fill:
        dict_to_fill["logger"].append(
            f"Multiple values for {parsed_value[1]} found. Line: {parsed_value.lineno(1)}")
        return
    try:
        dict_to_fill[argument_name] = method_to_apply(parsed_value[2])
    except SPDXParsingError as err:
        dict_to_fill["logger"].append(err.get_messages())
    except ValueError as err:
        dict_to_fill["logger"].append(err.args[0])
