# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from enum import auto

from spdx_tools.spdx.jsonschema.json_property import JsonProperty


class DocumentProperty(JsonProperty):
    SPDX_ID = auto()
    DOCUMENT_NAMESPACE = auto()
    NAME = auto()
    CREATION_INFO = auto()
    SPDX_VERSION = auto()
    DATA_LICENSE = auto()
    COMMENT = auto()
    EXTERNAL_DOCUMENT_REFS = auto()
    PACKAGES = auto()
    FILES = auto()
    SNIPPETS = auto()
    RELATIONSHIPS = auto()
    ANNOTATIONS = auto()
    HAS_EXTRACTED_LICENSING_INFOS = auto()
