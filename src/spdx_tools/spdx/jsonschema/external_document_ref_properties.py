# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from enum import auto

from spdx_tools.spdx.jsonschema.json_property import JsonProperty


class ExternalDocumentRefProperty(JsonProperty):
    EXTERNAL_DOCUMENT_ID = auto()
    SPDX_DOCUMENT = auto()
    CHECKSUM = auto()
