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

from typing import TextIO, Union, Optional


def write_value(tag: str, value: Optional[Union[bool, str]], out: TextIO, indent: bool = False):
    """ This function is duplicated from spdx.writer.tagvalue.tag_value_writer_helper_functions and slightly adapted to
        make indentation of output possible."""
    if not value:
        return
    if indent:
        out.write(f"\t{tag}: {value}\n")
    else:
        out.write(f"{tag}: {value}\n")
