# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from beartype.typing import Any, Type

from spdx_tools.spdx.jsonschema.converter import TypedConverter
from spdx_tools.spdx.jsonschema.extracted_licensing_info_properties import ExtractedLicensingInfoProperty
from spdx_tools.spdx.jsonschema.json_property import JsonProperty
from spdx_tools.spdx.jsonschema.optional_utils import apply_if_present
from spdx_tools.spdx.model import Document, ExtractedLicensingInfo


class ExtractedLicensingInfoConverter(TypedConverter[ExtractedLicensingInfo]):
    def _get_property_value(
        self,
        extracted_licensing_info: ExtractedLicensingInfo,
        extracted_licensing_info_property: ExtractedLicensingInfoProperty,
        document: Document = None,
    ) -> Any:
        if extracted_licensing_info_property == ExtractedLicensingInfoProperty.COMMENT:
            return extracted_licensing_info.comment
        elif extracted_licensing_info_property == ExtractedLicensingInfoProperty.EXTRACTED_TEXT:
            return extracted_licensing_info.extracted_text
        elif extracted_licensing_info_property == ExtractedLicensingInfoProperty.LICENSE_ID:
            return extracted_licensing_info.license_id
        elif extracted_licensing_info_property == ExtractedLicensingInfoProperty.NAME:
            return apply_if_present(str, extracted_licensing_info.license_name)
        elif extracted_licensing_info_property == ExtractedLicensingInfoProperty.SEE_ALSOS:
            return extracted_licensing_info.cross_references or None

    def get_json_type(self) -> Type[JsonProperty]:
        return ExtractedLicensingInfoProperty

    def get_data_model_type(self) -> Type[ExtractedLicensingInfo]:
        return ExtractedLicensingInfo
