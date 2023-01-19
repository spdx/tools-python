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

from spdx3.model.software.file import File
from spdx3.writer.console.artifact_writer import write_artifact_properties
from spdx3.writer.console.console import write_value


def write_file(file: File, text_output: TextIO):
    text_output.write("## File\n")
    write_artifact_properties(file, text_output)
    write_value("content_identifier", file.content_identifier, text_output)
    write_value("file_purpose", ", ".join([purpose.name for purpose in file.file_purpose]), text_output)
    write_value("content_type", file.content_type, text_output)
