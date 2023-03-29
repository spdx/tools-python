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
from typing import Type, Any

from spdx.jsonschema.converter import TypedConverter
from spdx.jsonschema.external_package_ref_properties import ExternalPackageRefProperty
from spdx.jsonschema.json_property import JsonProperty
from spdx.model.document import Document
from spdx.model.package import ExternalPackageRef


class ExternalPackageRefConverter(TypedConverter[ExternalPackageRef]):
    def _get_property_value(self, external_ref: ExternalPackageRef, external_ref_property: ExternalPackageRefProperty,
                            document: Document = None) -> Any:
        if external_ref_property == ExternalPackageRefProperty.COMMENT:
            return external_ref.comment
        elif external_ref_property == ExternalPackageRefProperty.REFERENCE_CATEGORY:
            return external_ref.category.name
        elif external_ref_property == ExternalPackageRefProperty.REFERENCE_LOCATOR:
            return external_ref.locator
        elif external_ref_property == ExternalPackageRefProperty.REFERENCE_TYPE:
            return external_ref.reference_type

    def get_json_type(self) -> Type[JsonProperty]:
        return ExternalPackageRefProperty

    def get_data_model_type(self) -> Type[ExternalPackageRef]:
        return ExternalPackageRef
