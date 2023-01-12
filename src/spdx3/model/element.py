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
from dataclasses import field
from typing import Optional, List

from common.typing.constructor_type_errors import ConstructorTypeErrors
from common.typing.type_checks import check_types_and_set_values
from common.typing.dataclass_with_properties import dataclass_with_properties

from spdx3.model.creation_information import CreationInformation
from spdx3.model.external_map import ExternalMap
from spdx3.model.namespace_map import NamespaceMap


@dataclass_with_properties
class Element:
    spdx_id: str  # IRI
    creation_info: CreationInformation
    name: Optional[str] = None
    summary: Optional[str] = None
    description: Optional[str] = None
    comment: Optional[str] = None
    verified_using: None = None  # placeholder for IntegrityMethod
    external_references: None = None  # placeholder for ExternalReference
    external_identifier: None = None  # placeholder for ExternalIdentifier
    extension: None = None  # placeholder for extension

    def __init__(self, spdx_id: str, creation_info: CreationInformation, name: Optional[str] = None,
                 summary: Optional[str] = None, description: Optional[str] = None, comment: Optional[str] = None,
                 verified_using: None = None, external_references: None = None, external_identifier: None = None,
                 extension: None = None):
        check_types_and_set_values(self, locals(), origin_class=Element)


@dataclass_with_properties
class Artifact(Element):
    originated_by: None = None  # placeholder for Actor

    def __init__(self, spdx_id: str, creation_info: CreationInformation, name: Optional[str] = None,
                 summary: Optional[str] = None, description: Optional[str] = None, comment: Optional[str] = None,
                 verified_using: None = None, external_references: None = None, external_identifier: None = None,
                 extension: None = None, originated_by: None = None):
        errors = []
        try:
            super().__init__(spdx_id, creation_info, name, summary, description, comment, verified_using,
                             external_references, external_identifier, extension)
        except ConstructorTypeErrors as err:
            errors.extend(err.get_messages())
        try:
            check_types_and_set_values(self, locals(), origin_class=Artifact)
        except ConstructorTypeErrors as err:
            errors.extend(err.get_messages())
        if errors:
            raise ConstructorTypeErrors(errors)

@dataclass_with_properties
class Collection(Element):
    namespace: Optional[NamespaceMap] = None
    imports: Optional[List[ExternalMap]] = field(default_factory=list)

    def __init__(self, spdx_id: str, creation_info: CreationInformation, name: Optional[str] = None,
                 summary: Optional[str] = None, description: Optional[str] = None, comment: Optional[str] = None,
                 verified_using: None = None, external_references: None = None, external_identifier: None = None,
                 extension: None = None, originated_by: None = None, namespace: Optional[NamespaceMap] = None,
                 imports: Optional[List[ExternalMap]] = None):
        imports = [] if imports is None else imports
        errors = []
        try:
            Element.__init__(self, spdx_id, creation_info, name, summary, description, comment, verified_using,
                         external_references, external_identifier, extension)
        except ConstructorTypeErrors as err:
            errors.extend(err.get_messages())
        try:
            check_types_and_set_values(self, locals(), origin_class=Collection)
        except ConstructorTypeErrors as err:
            errors.extend(err.get_messages())
        if errors:
            raise ConstructorTypeErrors(errors)


@dataclass_with_properties
class Bundle(Collection):
    context: Optional[str] = None

    def __init__(self, spdx_id: str, creation_info: CreationInformation, name: Optional[str] = None,
                 summary: Optional[str] = None, description: Optional[str] = None, comment: Optional[str] = None,
                 verified_using: None = None, external_references: None = None, external_identifier: None = None,
                 extension: None = None, originated_by: None = None, namespace: Optional[NamespaceMap] = None,
                 imports: Optional[List[ExternalMap]] = None, context: Optional[str] = None):
        errors = []
        try:
            Collection.__init__(self, spdx_id, creation_info, name, summary, description, comment, verified_using,
                                external_references, external_identifier, extension, originated_by, namespace,
                                imports)
        except ConstructorTypeErrors as err:
            errors.extend(err.get_messages())

        try:
            check_types_and_set_values(self, locals(), origin_class=Bundle)
        except ConstructorTypeErrors as err:
            errors.extend(err.get_messages())
        if errors:
            raise ConstructorTypeErrors(errors)


@dataclass_with_properties
class Bom(Bundle):
    def __init__(self, spdx_id: str, creation_info: CreationInformation, name: Optional[str] = None,
                 summary: Optional[str] = None, description: Optional[str] = None, comment: Optional[str] = None,
                 verified_using: None = None, external_references: None = None, external_identifier: None = None,
                 extension: None = None, originated_by: None = None, namespace: Optional[NamespaceMap] = None,
                 imports: Optional[List[ExternalMap]] = None, context: Optional[str] = None):
        errors = []
        try:
            Bundle.__init__(self, spdx_id, creation_info, name, summary, description, comment, verified_using,
                            external_references, external_identifier, extension, originated_by, namespace,
                            imports, context)
        except ConstructorTypeErrors as err:
            errors.extend(err.get_messages())
        try:
            check_types_and_set_values(self, locals(), origin_class=Bom)
        except ConstructorTypeErrors as err:
            errors.extend(err.get_messages())
        if errors:
            raise ConstructorTypeErrors(errors)
