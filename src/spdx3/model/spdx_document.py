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
from typing import Optional, List

from common.typing.type_checks import check_types_and_set_values

from spdx3.model.creation_information import CreationInformation

from common.typing.dataclass_with_properties import dataclass_with_properties
from spdx3.model.element import Element
from spdx3.model.bundle import Bundle
from spdx3.model.external_map import ExternalMap
from spdx3.model.integrity_method import IntegrityMethod
from spdx3.model.namespace_map import NamespaceMap


@dataclass_with_properties
class SpdxDocument(Bundle):
    # The inherited field "name" is required for a SpdxDocument, no longer optional.
    # We overwrite the super-__init__ as check_types_and_set_values() takes care of all fields (including inherited ones).
    def __init__(self, spdx_id: str, creation_info: CreationInformation, name: str, elements: List[str],
                 root_elements: List[str], summary: Optional[str] = None, description: Optional[str] = None,
                 comment: Optional[str] = None, verified_using: Optional[List[IntegrityMethod]] = None,
                 external_references: None = None, external_identifier: None = None, extension: None = None,
                 namespaces: Optional[List[NamespaceMap]] = None, imports: Optional[List[ExternalMap]] = None,
                 context: Optional[str] = None):
        verified_using = [] if verified_using is None else verified_using
        namespaces = [] if namespaces is None else namespaces
        imports = [] if imports is None else imports
        check_types_and_set_values(self, locals())
