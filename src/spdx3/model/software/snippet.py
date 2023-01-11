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
from typing import Optional, Tuple, List

from common.typing.constructor_type_errors import ConstructorTypeErrors
from common.typing.type_checks import check_types_and_set_values

from spdx3.model.creation_information import CreationInformation

from common.typing.dataclass_with_properties import dataclass_with_properties
from spdx3.model.software.software_purpose import SoftwarePurpose
from spdx3.model.element import Artifact


@dataclass_with_properties
class Snippet(Artifact):
    content_identifier: Optional[str] = None  # anyURI
    snippet_purpose: Optional[List[SoftwarePurpose]] = None
    byte_range: Optional[Tuple[int, int]] = None
    line_range: Optional[Tuple[int, int]] = None

    def __init__(self, spdx_id: str, creation_info: CreationInformation, name: Optional[str] = None,
                 summary: Optional[str] = None, description: Optional[str] = None, comment: Optional[str] = None,
                 verified_using: None = None, external_references: None = None, external_identifier: None = None,
                 extension: None = None, originated_by: None = None, content_identifier: Optional[str] = None,
                 snippet_purpose: Optional[List[SoftwarePurpose]] = None, byte_range: Optional[Tuple[int, int]] = None,
                 line_range: Optional[Tuple[int, int]] = None):
        snippet_purpose = [] if snippet_purpose is None else snippet_purpose
        errors = []
        try:
            Artifact.__init__(self, spdx_id, creation_info, name, summary, description, comment, verified_using,
                              external_references, external_identifier, extension, originated_by)
        except ConstructorTypeErrors as err:
            errors.extend(err.get_messages())
        try:
            check_types_and_set_values(self, locals())
        except ConstructorTypeErrors as err:
            errors.extend(err.get_messages())

        if errors:
            raise ConstructorTypeErrors(errors)
