# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from typing import TextIO

from spdx_tools.spdx3.model.software import Package
from spdx_tools.spdx3.writer.console.artifact_writer import write_artifact_properties
from spdx_tools.spdx3.writer.console.console import write_value


def write_package(package: Package, text_output: TextIO):
    text_output.write("## Package\n")
    write_artifact_properties(package, text_output)
    write_value("content_identifier", package.content_identifier, text_output)
    write_value("package_purpose", ", ".join([purpose.name for purpose in package.package_purpose]), text_output)
    write_value("package_version", package.package_version, text_output)
    write_value("download_location", package.download_location, text_output)
    write_value("package_uri", package.package_url, text_output)
    write_value("homepage", package.homepage, text_output)
