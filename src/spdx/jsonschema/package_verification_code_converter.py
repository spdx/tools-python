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
from spdx.jsonschema.json_property import JsonProperty
from spdx.jsonschema.package_verification_code_properties import PackageVerificationCodeProperty
from spdx.model.document import Document
from spdx.model.package import PackageVerificationCode


class PackageVerificationCodeConverter(TypedConverter[PackageVerificationCode]):
    def _get_property_value(self, verification_code: PackageVerificationCode,
                            verification_code_property: PackageVerificationCodeProperty,
                            document: Document = None) -> Any:
        if verification_code_property == PackageVerificationCodeProperty.PACKAGE_VERIFICATION_CODE_EXCLUDED_FILES:
            return verification_code.excluded_files or None
        elif verification_code_property == PackageVerificationCodeProperty.PACKAGE_VERIFICATION_CODE_VALUE:
            return verification_code.value

    def get_json_type(self) -> Type[JsonProperty]:
        return PackageVerificationCodeProperty

    def get_data_model_type(self) -> Type[PackageVerificationCode]:
        return PackageVerificationCode
