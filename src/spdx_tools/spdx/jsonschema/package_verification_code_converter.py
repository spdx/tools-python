# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from beartype.typing import Any, Type

from spdx_tools.spdx.jsonschema.converter import TypedConverter
from spdx_tools.spdx.jsonschema.json_property import JsonProperty
from spdx_tools.spdx.jsonschema.package_verification_code_properties import PackageVerificationCodeProperty
from spdx_tools.spdx.model import Document, PackageVerificationCode


class PackageVerificationCodeConverter(TypedConverter[PackageVerificationCode]):
    def _get_property_value(
        self,
        verification_code: PackageVerificationCode,
        verification_code_property: PackageVerificationCodeProperty,
        document: Document = None,
    ) -> Any:
        if verification_code_property == PackageVerificationCodeProperty.PACKAGE_VERIFICATION_CODE_EXCLUDED_FILES:
            return verification_code.excluded_files or None
        elif verification_code_property == PackageVerificationCodeProperty.PACKAGE_VERIFICATION_CODE_VALUE:
            return verification_code.value

    def get_json_type(self) -> Type[JsonProperty]:
        return PackageVerificationCodeProperty

    def get_data_model_type(self) -> Type[PackageVerificationCode]:
        return PackageVerificationCode
