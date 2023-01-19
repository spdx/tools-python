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

from spdx3.model.hash import Hash
from spdx3.writer.console.console import write_value
from spdx3.writer.console.integrity_method_writer import write_integrity_method


def write_hash(hash_object: Hash, text_output: TextIO, heading: bool, indent: bool = True):
    if heading:
        text_output.write("## Hash\n")
    write_value("algorithm", hash_object.algorithm.name, text_output, indent)
    write_value("hash_value", hash_object.hash_value, text_output, indent)
    write_integrity_method(hash_object, text_output, indent)
