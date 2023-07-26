# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from enum import auto

from spdx_tools.spdx.jsonschema.json_property import JsonProperty


class ExtractedLicensingInfoProperty(JsonProperty):
    LICENSE_ID = auto()
    NAME = auto()
    EXTRACTED_TEXT = auto()
    SEE_ALSOS = auto()
    COMMENT = auto()
