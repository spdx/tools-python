# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from enum import auto

from spdx_tools.spdx.jsonschema.json_property import JsonProperty


class ExtractedLicensingInfoProperty(JsonProperty):
    COMMENT = auto()
    EXTRACTED_TEXT = auto()
    LICENSE_ID = auto()
    NAME = auto()
    SEE_ALSOS = auto()
