# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from beartype.typing import TextIO

from spdx_tools.spdx3.model.ai import AIPackage
from spdx_tools.spdx3.writer.console.console import write_value
from spdx_tools.spdx3.writer.console.software.package_writer import write_package


def write_ai_package(ai_package: AIPackage, text_output: TextIO):
    text_output.write("## AI Package\n")
    write_package(ai_package, text_output, False)

    for property_name in AIPackage.__annotations__.keys():
        write_value(property_name, getattr(ai_package, property_name), text_output)
