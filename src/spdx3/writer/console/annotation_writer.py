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

from spdx3.model.annotation import Annotation
from spdx3.writer.console.console import write_value
from spdx3.writer.console.element_writer import write_element_properties


def write_annotation(annotation: Annotation, text_output: TextIO):
    text_output.write("## Annotation\n")
    write_element_properties(annotation, text_output)
    write_value("annotation_type", annotation.annotation_type.name, text_output)
    write_value("subject", annotation.subject, text_output)
    write_value("content_type", annotation.content_type, text_output)
    write_value("statement", annotation.statement, text_output)
