# SPDX-License-Identifier: Apache-2.0
#  Copyright (c) 2023 spdx contributors
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#      http://www.apache.org/licenses/LICENSE-2.0
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
from beartype.typing import TextIO

from spdx_tools.spdx3.model import Tool
from spdx_tools.spdx3.writer.console.element_writer import write_element_properties


def write_tool(tool: Tool, text_output: TextIO, heading: bool = True):
    if heading:
        text_output.write("## Tool\n")
    write_element_properties(tool, text_output)
