# SPDX-FileCopyrightText: 2022 spdx contributors

# SPDX-License-Identifier: Apache-2.0
from typing import Union

from license_expression import ExpressionError, LicenseExpression, Licensing

from spdx.model.spdx_no_assertion import SpdxNoAssertion
from spdx.model.spdx_none import SpdxNone
from spdx.parser.error import SPDXParsingError


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
