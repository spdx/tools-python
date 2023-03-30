# SPDX-FileCopyrightText: 2022 spdx contributors

# SPDX-License-Identifier: Apache-2.0
from enum import auto

from spdx.jsonschema.json_property import JsonProperty


class ExternalPackageRefProperty(JsonProperty):
    COMMENT = auto()
    REFERENCE_CATEGORY = auto()
    REFERENCE_LOCATOR = auto()
    REFERENCE_TYPE = auto()
