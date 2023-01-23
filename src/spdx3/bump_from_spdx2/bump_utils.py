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
from typing import Optional, Union

from spdx.model.spdx_no_assertion import SpdxNoAssertion
from spdx.model.spdx_none import SpdxNone


def handle_no_assertion_or_none(field: Union[SpdxNone, SpdxNoAssertion, str], field_name: str) -> Optional[str]:
    if isinstance(field, SpdxNone):
        print(f"{field_name}: Missing conversion for SpdxNone.")
        return None
    if isinstance(field, SpdxNoAssertion):
        return None
    if isinstance(field, str):
        return field
