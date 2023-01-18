# Copyright (c) 2023 spdx contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#    http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from typing import Optional, List

from common.typing.dataclass_with_properties import dataclass_with_properties
from common.typing.type_checks import check_types_and_set_values
from spdx3.model.creation_information import CreationInformation
from spdx3.model.element import Element
from spdx3.model.integrity_method import IntegrityMethod


@dataclass_with_properties
class Artifact(Element):
    # This should be an abstract class and should not be instantiated directly.
    # We need to investigate if we can combine dataclasses with abstract base classes (https://github.com/spdx/tools-python/issues/431)
    originated_by: None = None  # placeholder for Actor

    # We overwrite the super-__init__ as check_types_and_set_values() takes care of all fields (including inherited ones).
    def __init__(self, spdx_id: str, creation_info: CreationInformation, name: Optional[str] = None,
                 summary: Optional[str] = None, description: Optional[str] = None, comment: Optional[str] = None,
                 verified_using: Optional[List[IntegrityMethod]] = None, external_references: None = None,
                 external_identifier: None = None, extension: None = None, originated_by: None = None):
        check_types_and_set_values(self, locals())
