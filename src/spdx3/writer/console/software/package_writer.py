# Copyright (c) 2023 spdx contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#   http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from typing import TextIO

from spdx3.model.software.package import Package
from spdx3.writer.console.artifact_writer import write_artifact_properties
from spdx3.writer.console.console import write_value


def write_package(package: Package, text_output: TextIO):
    text_output.write("## Package\n")
    write_artifact_properties(package, text_output)
    write_value("content_identifier", package.content_identifier, text_output)
    write_value("package_purpose", ", ".join([purpose.name for purpose in package.package_purpose]), text_output)
    write_value("download_location", package.download_location, text_output)
    write_value("package_uri", package.package_uri, text_output)
    write_value("homepage", package.homepage, text_output)
