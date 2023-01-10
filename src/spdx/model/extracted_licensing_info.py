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
from typing import Optional, List, Union

from spdx.model.spdx_no_assertion import SpdxNoAssertion
from common.typing.dataclass_with_properties import dataclass_with_properties
from common.typing.type_checks import check_types_and_set_values


@dataclass_with_properties
class ExtractedLicensingInfo:
    license_id: Optional[str] = None
    extracted_text: Optional[str] = None
    license_name: Optional[Union[str, SpdxNoAssertion]] = None
    cross_references: List[str] = field(default_factory=list)
    comment: Optional[str] = None

    def __init__(self, license_id: Optional[str] = None, extracted_text: Optional[str] = None,
                 license_name: Optional[Union[str, SpdxNoAssertion]] = None, cross_references: List[str] = None,
                 comment: Optional[str] = None):
        cross_references = [] if cross_references is None else cross_references
        check_types_and_set_values(self, locals())
