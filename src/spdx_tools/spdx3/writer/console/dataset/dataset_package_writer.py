# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from beartype.typing import TextIO

from spdx_tools.spdx3.model.dataset import DatasetPackage
from spdx_tools.spdx3.writer.console.console import write_value
from spdx_tools.spdx3.writer.console.software.package_writer import write_package


def write_dataset_package(datasetPackage: DatasetPackage, text_output: TextIO):
    text_output.write("## Dataset\n")
    write_package(datasetPackage, text_output, False)

    for property_name in DatasetPackage.__annotations__.keys():
        write_value(property_name, getattr(datasetPackage, property_name), text_output)
