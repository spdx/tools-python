# Copyright (c) 2022 spdx contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from typing import Tuple, Optional, List

from src.model.license_expression import LicenseExpression
from src.model.spdx_no_assertion import SpdxNoAssertion
from src.model.spdx_none import SpdxNone


class Snippet:
    spdx_id: str
    file_spdx_id: str
    byte_range: Tuple[int, int]
    line_range: Optional[Tuple[int, int]]
    concluded_license: Optional[LicenseExpression, SpdxNoAssertion, SpdxNone]
    license_info_in_snippet: Optional[List[LicenseExpression], SpdxNoAssertion, SpdxNone]
    license_comment: Optional[str]
    copyright_text: Optional[str]
    comment: Optional[str]
    name: Optional[str]
    attribution_texts: List[str]

    def __init__(self, spdx_id: str, file_spdx_id: str, byte_range: Tuple[int, int],
                 line_range: Optional[Tuple[int, int]] = None,
                 concluded_license: Optional[LicenseExpression, SpdxNoAssertion, SpdxNone] = None,
                 license_info_in_snippet: Optional[List[LicenseExpression], SpdxNoAssertion, SpdxNone] = None,
                 license_comment: Optional[str] = None, copyright_text: Optional[str] = None,
                 comment: Optional[str] = None, name: Optional[str] = None, attribution_texts: List[str] = None):
        self.spdx_id = spdx_id
        self.file_spdx_id = file_spdx_id
        self.byte_range = byte_range
        self.line_range = line_range
        self.concluded_license = concluded_license
        self.license_info_in_snippet = license_info_in_snippet
        self.license_comment = license_comment
        self.copyright_text = copyright_text
        self.comment = comment
        self.name = name
        self.attribution_texts = [] if attribution_texts is None else attribution_texts
