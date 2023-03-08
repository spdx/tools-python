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

from ply.yacc import YaccProduction

from spdx.model.checksum import Checksum, ChecksumAlgorithm
from spdx.parser.error import SPDXParsingError


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


def parse_checksum(checksum_str: str) -> Checksum:
    # The lexer and the corresponding regex for the token CHECKSUM and EXT_DOC_REF_CHECKSUM ensure that the passed
    # checksum_str is formatted in the way that the following lines of code can't cause an error.
    algorithm, value = checksum_str.split(":")
    algorithm = ChecksumAlgorithm[algorithm.upper().replace("-", "_")]
    value = value.strip()
    checksum = Checksum(algorithm, value)
    return checksum


def set_value(parsed_value: YaccProduction, dict_to_fill: Dict[str, Any], argument_name: Optional[str] = None,
              method_to_apply: Callable = lambda x: x):
    # Parsed_value.slice returns a List of the objects in the corresponding grammar_rule for the parsed value,
    # e.g. for @grammar_rule("created : CREATED DATE") the return value is something like
    # p.slice = ["created", LexToken(CREATED,..), LexToken(DATE,..)].
    # So the first value is the name of the grammar_rule that we have named according to the field in the data model.
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
