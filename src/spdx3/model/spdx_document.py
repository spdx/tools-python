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

from common.typing.constructor_type_errors import ConstructorTypeErrors

from spdx3.model.creation_information import CreationInformation

from common.typing.dataclass_with_properties import dataclass_with_properties
from spdx3.model.element import Bundle
from spdx3.model.external_map import ExternalMap
from spdx3.model.namespace_map import NamespaceMap


@dataclass_with_properties
class SpdxDocument(Bundle):
    # inherited field name is required for a SpdxDocument, no longer optional
    def __init__(self, spdx_id: str, creation_info: CreationInformation, name: str,
                 summary: Optional[str] = None, description: Optional[str] = None, comment: Optional[str] = None,
                 verified_using: None = None, external_references: None = None, external_identifier: None = None,
                 extension: None = None, originated_by: None = None, namespace: Optional[NamespaceMap] = None,
                 import_element: Optional[List[ExternalMap]] = None, context: Optional[str] = None):
        errors = []
        try:
            super().__init__(spdx_id, creation_info, name, summary, description, comment, verified_using,
                        external_references, external_identifier, extension, originated_by, namespace,
                        import_element, context)
        except ConstructorTypeErrors as err:
            errors.extend(err.get_messages())
        try:
            check_types_and_set_values(self, locals(), origin_class=SpdxDocument)
        except ConstructorTypeErrors as err:
            errors.extend(err.get_messages())
        if errors:
            raise ConstructorTypeErrors(errors)
