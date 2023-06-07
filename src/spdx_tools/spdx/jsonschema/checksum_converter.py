# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from beartype.typing import Type

from spdx_tools.spdx.jsonschema.checksum_properties import ChecksumProperty
from spdx_tools.spdx.jsonschema.converter import TypedConverter
from spdx_tools.spdx.jsonschema.json_property import JsonProperty
from spdx_tools.spdx.model import Checksum, ChecksumAlgorithm, Document


class ChecksumConverter(TypedConverter[Checksum]):
    def get_data_model_type(self) -> Type[Checksum]:
        return Checksum

    def get_json_type(self) -> Type[JsonProperty]:
        return ChecksumProperty

    def _get_property_value(
        self, checksum: Checksum, checksum_property: ChecksumProperty, _document: Document = None
    ) -> str:
        if checksum_property == ChecksumProperty.ALGORITHM:
            return algorithm_to_json_string(checksum.algorithm)
        elif checksum_property == ChecksumProperty.CHECKSUM_VALUE:
            return checksum.value


def algorithm_to_json_string(algorithm: ChecksumAlgorithm) -> str:
    name_with_dash: str = algorithm.name.replace("_", "-")
    if "BLAKE2B" in name_with_dash:
        return name_with_dash.replace("BLAKE2B", "BLAKE2b")
    return name_with_dash
