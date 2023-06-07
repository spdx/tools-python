# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from beartype.typing import Any, Type

from spdx_tools.spdx.jsonschema.converter import TypedConverter
from spdx_tools.spdx.jsonschema.external_package_ref_properties import ExternalPackageRefProperty
from spdx_tools.spdx.jsonschema.json_property import JsonProperty
from spdx_tools.spdx.model import Document, ExternalPackageRef


class ExternalPackageRefConverter(TypedConverter[ExternalPackageRef]):
    def _get_property_value(
        self,
        external_ref: ExternalPackageRef,
        external_ref_property: ExternalPackageRefProperty,
        document: Document = None,
    ) -> Any:
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
