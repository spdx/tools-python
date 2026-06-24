# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from beartype.typing import TextIO

from spdx_tools.spdx3.model.dataset import DatasetPackage
from spdx_tools.spdx3.writer.console.console import write_value
from spdx_tools.spdx3.writer.console.software.package_writer import write_package


def write_dataset(dataset: DatasetPackage, text_output: TextIO):
    text_output.write("## DatasetPackage\n")
    write_package(dataset, text_output, False)

    for property_name in DatasetPackage.__annotations__.keys():
        write_value(property_name, getattr(dataset, property_name), text_output)
