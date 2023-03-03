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
from dataclasses import field
from typing import Tuple, Optional, List, Union

from common.typing.dataclass_with_properties import dataclass_with_properties
from license_expression import LicenseExpression
from spdx.model.spdx_no_assertion import SpdxNoAssertion
from spdx.model.spdx_none import SpdxNone
from common.typing.type_checks import check_types_and_set_values


@dataclass_with_properties
class Snippet:
    spdx_id: str
    file_spdx_id: str
    byte_range: Tuple[int, int]
    line_range: Optional[Tuple[int, int]] = None
    license_concluded: Optional[Union[LicenseExpression, SpdxNoAssertion, SpdxNone]] = None
    license_info_in_snippet: List[Union[LicenseExpression, SpdxNoAssertion, SpdxNone]] = None
    license_comment: Optional[str] = None
    copyright_text: Optional[Union[str, SpdxNoAssertion, SpdxNone]] = None
    comment: Optional[str] = None
    name: Optional[str] = None
    attribution_texts: List[str] = field(default_factory=list)

    def __init__(self, spdx_id: str, file_spdx_id: str, byte_range: Tuple[int, int],
                 line_range: Optional[Tuple[int, int]] = None,
                 license_concluded: Optional[Union[LicenseExpression, SpdxNoAssertion, SpdxNone]] = None,
                 license_info_in_snippet: List[Union[LicenseExpression, SpdxNoAssertion, SpdxNone]] = None,
                 license_comment: Optional[str] = None, copyright_text: Optional[str] = None,
                 comment: Optional[str] = None, name: Optional[str] = None, attribution_texts: List[str] = None):
        attribution_texts = [] if attribution_texts is None else attribution_texts
        license_info_in_snippet = [] if license_info_in_snippet is None else license_info_in_snippet
        check_types_and_set_values(self, locals())
