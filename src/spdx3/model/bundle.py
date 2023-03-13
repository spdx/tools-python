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
from spdx3.model.external_identifier import ExternalIdentifier
from spdx3.model.external_map import ExternalMap
from spdx3.model.external_reference import ExternalReference
from spdx3.model.integrity_method import IntegrityMethod
from spdx3.model.namespace_map import NamespaceMap
from spdx3.model.spdx_collection import SpdxCollection


@dataclass_with_properties
class Bundle(SpdxCollection):
    context: Optional[str] = None

    def __init__(self, spdx_id: str, creation_info: CreationInformation, elements: List[str],
                 root_elements: List[str], name: Optional[str] = None, summary: Optional[str] = None,
                 description: Optional[str] = None, comment: Optional[str] = None,
                 verified_using: Optional[List[IntegrityMethod]] = None,
                 external_references: Optional[List[ExternalReference]] = None,
                 external_identifier: Optional[List[ExternalIdentifier]] = None, extension: None = None,
                 namespaces: Optional[List[NamespaceMap]] = None,
                 imports: Optional[List[ExternalMap]] = None, context: Optional[str] = None):
        verified_using = [] if verified_using is None else verified_using
        external_references = [] if external_references is None else external_references
        external_identifier = [] if external_identifier is None else external_identifier
        namespaces = [] if namespaces is None else namespaces
        imports = [] if imports is None else imports
        check_types_and_set_values(self, locals())
