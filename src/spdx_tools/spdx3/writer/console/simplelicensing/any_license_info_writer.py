from beartype.typing import TextIO

from spdx_tools.spdx3.model.simplelicensing.license_expression import AnyLicenseInfo
from spdx_tools.spdx3.writer.console.element_writer import write_element_properties


def write_any_license_info(any_license_info: AnyLicenseInfo, text_output: TextIO, heading: bool = True):
    if heading:
        text_output.write("## AnyLicenseInfo\n")
    write_element_properties(any_license_info, text_output)
