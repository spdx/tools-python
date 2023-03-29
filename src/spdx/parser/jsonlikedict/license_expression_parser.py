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
from typing import Union, List

from license_expression import LicenseExpression, Licensing, ExpressionError

from spdx.model.spdx_no_assertion import SpdxNoAssertion
from spdx.model.spdx_none import SpdxNone
from spdx.parser.error import SPDXParsingError
from spdx.parser.jsonlikedict.dict_parsing_functions import append_parsed_field_or_log_error
from spdx.parser.parsing_functions import raise_parsing_error_if_logger_has_messages
from spdx.parser.logger import Logger


class LicenseExpressionParser:
    @staticmethod
    def parse_license_expression(license_expression_str: str) -> Union[LicenseExpression, SpdxNone, SpdxNoAssertion]:
        if isinstance(license_expression_str, str):
            if license_expression_str.upper() == "NOASSERTION":
                return SpdxNoAssertion()
            if license_expression_str.upper() == "NONE":
                return SpdxNone()

        try:
            license_expression = Licensing().parse(license_expression_str)
        except ExpressionError as err:
            raise SPDXParsingError([f"Error parsing LicenseExpression: {err.args[0]}: {license_expression_str}"])

        return license_expression
