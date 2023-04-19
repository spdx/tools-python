# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from enum import auto

from spdx_tools.spdx.jsonschema.json_property import JsonProperty


class CreationInfoProperty(JsonProperty):
    CREATED = auto()
    CREATORS = auto()
    LICENSE_LIST_VERSION = auto()
    COMMENT = auto()
