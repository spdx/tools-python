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

from spdx3.model.relationship import Relationship
from spdx3.writer.console.console import write_value


def write_relationship(relationship: Relationship, text_output: TextIO):
    text_output.write("## Relationship\n")
    write_value("from_element", relationship.from_element, text_output)
    write_value("to", ", ".join(relationship.to), text_output)
    write_value("relationship_type", relationship.relationship_type.name, text_output)
    write_value("completeness", relationship.completeness.name, text_output)
