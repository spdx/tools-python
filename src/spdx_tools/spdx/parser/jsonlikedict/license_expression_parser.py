# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from beartype.typing import Union
from license_expression import ExpressionError, LicenseExpression

from spdx_tools.common.spdx_licensing import spdx_licensing
from spdx_tools.spdx.model import SpdxNoAssertion, SpdxNone
from spdx_tools.spdx.parser.error import SPDXParsingError


class LicenseExpressionParser:
    @staticmethod
    def parse_license_expression(license_expression_str: str) -> Union[LicenseExpression, SpdxNone, SpdxNoAssertion]:
        if isinstance(license_expression_str, str):
            if license_expression_str.upper() == "NOASSERTION":
                return SpdxNoAssertion()
            if license_expression_str.upper() == "NONE":
                return SpdxNone()

        try:
            license_expression = spdx_licensing.parse(license_expression_str)
        except ExpressionError as err:
            err_msg = f'Error parsing LicenseExpression: "{license_expression_str}"'
            if err.args:
                err_msg += f": {err.args[0]}"
            raise SPDXParsingError([err_msg])

        return license_expression
