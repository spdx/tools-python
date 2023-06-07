# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from beartype.typing import Any, Dict

from spdx_tools.common.typing.constructor_type_errors import ConstructorTypeErrors
from spdx_tools.spdx.parser.error import SPDXParsingError
from spdx_tools.spdx.parser.logger import Logger


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
