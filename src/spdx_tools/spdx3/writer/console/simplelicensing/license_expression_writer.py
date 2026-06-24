from beartype.typing import TextIO

from spdx_tools.spdx3.model.simplelicensing.license_expression import LicenseExpression
from spdx_tools.spdx3.writer.console.console import write_value
from spdx_tools.spdx3.writer.console.simplelicensing.any_license_info_writer import write_any_license_info


def write_license_expression(license_expression: LicenseExpression, text_output: TextIO):
    text_output.write("## LicenseExpression\n")
    write_any_license_info(license_expression, text_output, False)

    for property_name in LicenseExpression.__annotations__.keys():
        write_value(property_name, getattr(license_expression, property_name), text_output)
