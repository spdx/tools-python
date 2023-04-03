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

from spdx3.model.creation_information import CreationInformation
from spdx3.writer.console.console import write_value
from spdx.datetime_conversions import datetime_to_iso_string


def write_creation_info(creation_info: CreationInformation, text_output: TextIO, indent: bool = True):
    text_output.write("# Creation Information\n")
    write_value("specVersion", str(creation_info.spec_version), text_output, indent)
    write_value("created", datetime_to_iso_string(creation_info.created), text_output, indent)
    for created_by in creation_info.created_by:
        write_value("created by", created_by, text_output, indent)
    for created_using in creation_info.created_using:
        write_value("created using", created_using, text_output, indent)
    write_value("profile", ", ".join(creation_info.profile), text_output, indent)
    write_value("data license", creation_info.data_license, text_output, indent)
