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

from src.model.license_expression import LicenseExpression
from src.model.spdx_no_assertion import SpdxNoAssertion
from src.model.spdx_none import SpdxNone
from src.parser.error import SPDXParsingError
from src.parser.json.dict_parsing_functions import construct_or_raise_parsing_error, append_parsed_field_or_log_error, \
    raise_parsing_error_if_logger_has_messages
from src.parser.logger import Logger


class LicenseExpressionParser:
    def parse_license_expression(self, license_expression_str_or_list: Union[str, List[str]]) -> Union[
        LicenseExpression, SpdxNoAssertion, SpdxNone, List[LicenseExpression]]:
        if license_expression_str_or_list == SpdxNone().__str__():
            return SpdxNone()
        if license_expression_str_or_list == SpdxNoAssertion().__str__():
            return SpdxNoAssertion()
        elif isinstance(license_expression_str_or_list, list):
            return self.parse_license_expressions(license_expression_str_or_list)

        else:
            license_expression = construct_or_raise_parsing_error(LicenseExpression,
                                                                  dict(
                                                                      expression_string=license_expression_str_or_list))
            return license_expression

    def parse_license_expressions(self, license_expression_str_or_list: List[str]) -> List[LicenseExpression]:
        license_expressions = []
        logger = Logger()
        for license_expression_str in license_expression_str_or_list:
            try:
                license_expressions = append_parsed_field_or_log_error(logger, license_expressions,
                                                                       license_expression_str,
                                                                       self.parse_license_expression)
            except SPDXParsingError as err:
                logger.append(err.get_messages())
        raise_parsing_error_if_logger_has_messages(logger)
        return license_expressions
