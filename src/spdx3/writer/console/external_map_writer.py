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

from spdx3.model.external_map import ExternalMap
from spdx3.writer.console.console import write_value
from spdx3.writer.console.hash_writer import write_hash
from spdx.writer.tagvalue.tagvalue_writer_helper_functions import write_optional_heading


def write_external_map(external_map: ExternalMap, text_output: TextIO):
    write_value("external_id", external_map.external_id, text_output)
    write_optional_heading(external_map.verified_using, "verified using\n", text_output)
    for integrity_method in external_map.verified_using:
        # for now Hash is the only child class of the abstract class IntegrityMethod,
        # as soon as there are more inherited classes we need to implement a logic
        # that determines the correct write function for the "integrity_method" object
        write_hash(integrity_method, text_output, heading=False)
    write_value("location_hint", external_map.location_hint, text_output)
